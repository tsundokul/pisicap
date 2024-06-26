import httpx
import logging
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed

from . import utils

# from pprint import pprint as print


class SICAP:
    retry_rules = dict(
        retry=retry_if_result(utils.not_200),
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
    )

    def __init__(
        self, secure: bool = True, timeout: httpx.Timeout = None, verbose: bool = False
    ) -> None:
        add_tls = "s" if secure else ""
        logging.basicConfig(level=logging.INFO if verbose else logging.ERROR)

        self.session = httpx.Client(
            base_url=f"http{add_tls}://e-licitatie.ro/api-pub",
            headers={
                "Referer": "https://e-licitatie.ro",
                "Content-Type": "application/json;charset=UTF-8",
            },
            timeout=timeout or httpx.Timeout(60.0, connect=10.0),
        )

        logging.info("pisciap API initialized 😼")

    def getServerTime(self) -> str:
        """Returns server time as string e.g. 2023-06-01T00:00:00.000Z"""
        return self.session.get("/time/getServerTime").text

    @retry(**retry_rules)
    def getCANoticeList(self, body_params_overrides: dict = {}) -> httpx.Response:
        """Returns a list of notices based on given filters"""
        body = {
            "sysNoticeTypeIds": [],
            "sortProperties": [],
            "pageSize": 2000,
            "sysNoticeStateId": None,
            "contractingAuthorityId": None,
            "winnerId": None,
            "cPVCategoryId": None,
            "sysContractAssigmentTypeId": None,
            "cPVId": None,
            "assignedUserId": None,
            "sysAcquisitionContractTypeId": None,
            "pageIndex": 0,
            "startPublicationDate": utils.yesterday(),
            "endPublicationDate": None,
        }

        body.update(body_params_overrides)
        return self.session.post("/NoticeCommon/GetCANoticeList/", json=body)

    @retry(**retry_rules)
    def getCANotice(self, caNoticeId: int) -> httpx.Response:
        """Returns public notice document"""
        return self.session.get(f"C_PUBLIC_CANotice/get/{caNoticeId}")

    @retry(**retry_rules)
    def getCANoticeContracts(self, body_params_overrides: dict = {}) -> httpx.Response:
        """Returns contracts within a public notice"""
        body = {
            "caNoticeId": 0,
            "winnerTitle": None,
            "winnerFiscalNumber": None,
            "contractDate": {
                "from": None,
                "to": None,
            },
            "contractValue": {
                "from": None,
                "to": None,
            },
            "contractMinOffer": {
                "from": None,
                "to": None,
            },
            "contractMaxOffer": {
                "from": None,
                "to": None,
            },
            "contractTitle": None,
            "lots": None,
            "sortOrder": [],
            "sysContractFrameworkType": {},
            "skip": 0,
            "take": 200,
        }

        body.update(body_params_overrides)
        return self.session.post("/C_PUBLIC_CANotice/GetCANoticeContracts", json=body)

    @retry(**retry_rules)
    def getPUBLICPINoticeAll(self, body_params_overrides: dict = {}) -> httpx.Response:
        """Returns priorinformation notices"""
        body = {"pageIndex": 0, "pageSize": 18, "sortProperties": [], "cpv": None}
        body.update(body_params_overrides)

        return self.session.post("/PUBLICPINotice/GetAll/", json=body)

    @retry(**retry_rules)
    def getCNoticeList(self, body_params_overrides: dict = {}) -> httpx.Response:
        body = {
            "sysNoticeTypeIds": [],
            "sortProperties": [],
            "pageSize": 5,
            "hasUnansweredQuestions": False,
            "pageIndex": 0,
            "startTenderReceiptDeadline": None,
            "sysProcedureStateId": 2,
            "sysProcedurePhaseId": 4,
            "startPublicationDate": None,
            "endPublicationDate": None,
        }
        # sysProcedurePhaseId
        # 9: "Submit Application"
        # 10: "Evaluate Application"
        # 2: "Submit Bid"
        # 3: "Evaluate Qualification and Technical"
        # 11: "Financial Evaluation"
        # 12: "Re-bidding"
        # 6: "Electronic Auction"
        # 4 "Deliberation"
        # 5: "Awarded"
        # 2 (without a label)

        body.update(body_params_overrides)
        return self.session.post("/NoticeCommon/GetCNoticeList/", json=body)

    @retry(**retry_rules)
    def getProcedureView(
        self, proc_id: int, params_overrides: dict = {}
    ) -> httpx.Response:
        params = {"procedureId": proc_id, "procedureLotId": "undefined"}
        params.update(params_overrides)

        return self.session.get("PUBLICProcedure/GetProcedureView/", params=params)

    @retry(**retry_rules)
    def getDaAwardNoticeList(self, body_params_overrides: dict = {}) -> httpx.Response:
        body = {
            "pageSize": 5,
            "publicationDateStart": utils.yesterday(),
            "pageIndex": 0,
            # "noticeNo": "number",
            # "contractObject": "procurement",
            # "awardedValueStart": 0,
            # "awardedValueEnd": 0.01,
            # "publicationDateEnd": "2024-01-15T22:00:00.000Z",
            # "cpvCodeText": "cpv"
        }

        body.update(body_params_overrides)
        return self.session.post(
            "/DaAwardNoticeCommon/GetDaAwardNoticeList/", json=body
        )

    @retry(**retry_rules)
    def getPublicDAAwardNotice(self, notice_id: int) -> httpx.Response:
        return self.session.get(f"/PublicDAAwardNotice/getView/{notice_id}")

    @retry(**retry_rules)
    def getCAEntityView(self, ca_entity_id: int) -> httpx.Response:
        return self.session.get(f"/Entity/getCAEntityView/{ca_entity_id}")

    @retry(**retry_rules)
    def getSUEntityView(self, su_entity_id: int) -> httpx.Response:
        return self.session.get(f"/Entity/getSUEntityView/{su_entity_id}")

    @retry(**retry_rules)
    def getDirectAcquisitionList(
        self, body_params_overrides: dict = {}
    ) -> httpx.Response:
        body = {
            "pageSize": 2000,
            "showOngoingDa": False,
            "cookieContext": None,
            "pageIndex": 0,
            "sysDirectAcquisitionStateId": None,
            "publicationDateStart": None,
            "publicationDateEnd": None,
            "finalizationDateStart": utils.yesterday(),
            "finalizationDateEnd": None,
            "cpvCategoryId": None,
            "contractingAuthorityId": None,
            "supplierId": None,
            "cpvCodeId": None,
        }

        body.update(body_params_overrides)
        return self.session.post(
            "/DirectAcquisitionCommon/GetDirectAcquisitionList/", json=body
        )

    @retry(**retry_rules)
    def getPublicDirectAcquisition(self, da_id) -> httpx.Response:
        return self.session.get(f"/PublicDirectAcquisition/getView/{da_id}")

    @retry(**retry_rules)
    def getRfqInvitationView(self, invitation_id: int) -> httpx.Response:
        return self.session.get(
            f"/PublicRFQInvitation/getRfqInvitationView/?rfqInvitationId={invitation_id}"
        )

    @retry(**retry_rules)
    def getProcedureReports(self, proc_id: int) -> httpx.Response:
        return self.session.get(
            f"/PUBLICProcedure/GetProcedureReports/?procedureId={proc_id}"
        )

    @retry(**retry_rules)
    def getProcedureStatementView(self, proc_st_id: int) -> httpx.Response:
        return self.session.get(
            f"/PUBLICProcedure/GetProcedureStatementView/?procedureStatementId={proc_st_id}"
        )

    def cpvs(self) -> dict:
        if not hasattr(self, "__cpvs"):
            self.__cpvs = utils.read_cpvs()

        return self.__cpvs
