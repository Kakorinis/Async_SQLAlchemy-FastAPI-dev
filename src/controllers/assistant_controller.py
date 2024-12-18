from typing import List

from src.repositories import AssistantRepository
from src.schemas.dtos import BillSchema
from src.schemas.responses import ApartmentFullResponse, DebtorInfoResponse
from settings import app_settings
from src.schemas.responses import DebtorMessageResponse
from src.schemas.responses.apartments_debt_schema import ApartmentsDebtSchema


class AssistantController:

    def __init__(self, main_repository: AssistantRepository):
        self.main_repository = main_repository

    # TODO после реализации специфичных селектов в AssistantRepository, контроллер получит свои методы, а пока
    # нужны только мапперы

    @staticmethod
    def map_data_to_debtor_message(dto: ApartmentFullResponse) -> DebtorMessageResponse:
        """
        Метод собирает форму для отправки должнику, где указаны детали должника и характер задолженности.

        :param dto: дто с полными данными о квартире, ее собственнике и списке неоплаченных счетов.
        :return: дто с параметром data, где содержится текст для отправки должнику.
        """
        debtor = dto.owner.fullname
        debtor_address = f'{dto.building.address}, кв {dto.apartment_number}'
        common_debt = sum([dto_.bill_size for dto_ in dto.bills])
        all_periods_data = ''
        for dto_ in dto.bills:
            debt_data = f'- {dto_.bill_period}: {dto_.bill_size} \n'
            if debt_data.startswith('    '):
                debt_data = f'    {debt_data}'
            all_periods_data += debt_data

        message = app_settings.DEBTOR_MESSAGE_TEMPLATE.format(
            debtor,
            debtor_address,
            debtor,
            common_debt,
            all_periods_data
        )
        return DebtorMessageResponse(data=message)

    @staticmethod
    def map_debtors_info_response(
            dtos: List[ApartmentFullResponse],
            sort_flag: bool = False
    ) -> List[DebtorInfoResponse]:
        """
        Маппинг дто DebtorInfoResponse из дто ApartmentFullResponse.

        :param dtos: дто-шки ApartmentFullResponse
        :param sort_flag: необходимость сортировки по убыванию суммы.
        :return: список DebtorInfoResponse.
        """
        result = list()
        person_apart_dict = dict()

        for dto in dtos:  # этап получения уникальных собственников и всех их квартир
            key_ = f'{dto.owner.fullname}-{dto.owner.phone}-{dto.owner.id}'
            if person_apart_dict.get(key_):
                person_apart_dict[key_].append(dto)
            else:
                person_apart_dict[key_] = [dto]

        for person_key, full_dtos_list in person_apart_dict.items():
            common_debt = 0
            apartments_list = list()
            for dto in full_dtos_list:
                common_one_apart_debt = 0
                bills_list = list()

                for bill_dto in dto.bills:
                    common_debt += bill_dto.bill_size
                    common_one_apart_debt += bill_dto.bill_size
                    bills_list.append(
                        BillSchema.model_validate(bill_dto)
                    )

                apartments_list.append(
                    ApartmentsDebtSchema(
                        **dto.__dict__,
                        address=dto.building.address,
                        project_name=dto.building.project_name,
                        common_debt=common_one_apart_debt,
                        bills_not_payed=bills_list
                    )

                )
            person_phone_splited = person_key.split('-')
            result.append(
                DebtorInfoResponse(
                    id_owner=int(person_phone_splited[2]),
                    fullname=person_phone_splited[0],
                    phone=person_phone_splited[1],
                    all_aparts_common_debt=common_debt,
                    apartments_debt=apartments_list
                )
            )
            if sort_flag and result:
                result.sort(key=lambda model: model.all_aparts_common_debt, reverse=True)
        return result
