import httpx
import logging

from . import utils

# from pprint import pprint as print


class SICAP:
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

    def getCANotice(self, caNoticeId: int) -> httpx.Response:
        """Returns public notice document"""
        return self.session.get(f"C_PUBLIC_CANotice/get/{caNoticeId}")

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

    def getPUBLICPINoticeAll(self, body_params_overrides: dict = {}) -> httpx.Response:
        """Returns priorinformation notices"""
        body = {"pageIndex": 0, "pageSize": 18, "sortProperties": [], "cpv": None}
        body.update(body_params_overrides)

        return self.session.post("/PUBLICPINotice/GetAll/", json=body)

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
