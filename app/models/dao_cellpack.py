from phmconfig.dataConvertUtil import DataConvertUtil
from services.main import AppCRUD
from models.tables import TCellPack
from schemas.vrla.cellpack_model import CellPackModel
from sqlalchemy import and_, desc


class CellPackCRUD(AppCRUD):
    """
    装备评估CRUD
    """

    def create_record(self, item: CellPackModel) -> TCellPack:
        """
        创建一条记录
        """
        record = TCellPack(ts=item.ts,
                           did=item.did,
                           dclz=item.dclz,
                           reqId=item.reqId,

                           M01=item.M01,
                           M02=item.M02,
                           M03=item.M03,
                           M04=item.M04,
                           M05=item.M05,
                           M06=item.M06,
                           M07=item.M07,
                           M08=item.M08,
                           M09=item.M09,
                           M10=item.M10,
                           M11=item.M11,
                           M12=item.M12,
                           M13=item.M13,
                           M14=item.M14,
                           M15=item.M15,
                           M16=item.M16,
                           M17=item.M17,
                           M18=item.M18,
                           M19=item.M19,
                           M20=item.M20,
                           M21=item.M21,
                           M22=item.M22,
                           M23=item.M23,
                           M24=item.M24,
                           M25=item.M25,
                           M26=item.M26,
                           M27=item.M27,
                           M28=item.M28,
                           M29=item.M29,
                           M30=item.M30,
                           M31=item.M31,
                           M32=item.M32,
                           M33=item.M33,
                           M34=item.M34,
                           M35=item.M35,
                           M36=item.M36,
                           M37=item.M37,
                           M38=item.M38,
                           M39=item.M39,

                           AM1=item.AM1,
                           AM2=item.AM2,
                           AM3=item.AM3,
                           AM4=item.AM4,
                           AM5=item.AM5,

                           IM1=item.IM1,

                           FM1=item.FM1,
                           FM2=item.FM2,
                           FM3=item.FM3,
                           FM4=item.FM4,
                           FM5=item.FM5
                           )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def create_batch(self, reqid, items, clz) -> TCellPack:
        """
        批量创建记录
        """
        records = []
        for im in items:
            item = DataConvertUtil.SOH(reqid, im)
            record = TCellPack(ts=item["ts"],
                               did=item["did"],
                               dclz=clz,
                               reqId=reqid,
                               M01=item["M01"],
                               M02=item["M02"],
                               M03=item["M03"],
                               M04=item["M04"],
                               M05=item["M05"],
                               M06=item["M06"],
                               M07=item["M07"],
                               M08=item["M08"],
                               M09=item["M09"],
                               M10=item["M10"],
                               M11=item["M11"],
                               M12=item["M12"],
                               M13=item["M13"],
                               M14=item["M14"],
                               M15=item["M15"],
                               M16=item["M16"],
                               M17=item["M17"],
                               M18=item["M18"],
                               M19=item["M19"],
                               M20=item["M20"],
                               M21=item["M21"],
                               M22=item["M22"],
                               M23=item["M23"],
                               M24=item["M24"],
                               M25=item["M25"],
                               M26=item["M26"],
                               M27=item["M27"],
                               M28=item["M28"],
                               M29=item["M29"],
                               M30=item["M30"],
                               M31=item["M31"],
                               M32=item["M32"],
                               M33=item["M33"],
                               M34=item["M34"],
                               M35=item["M35"],
                               M36=item["M36"],
                               M37=item["M37"],
                               M38=item["M38"],
                               M39=item["M39"],
                               IM1=item["IM1"],
                               AM1=item["AM1"],
                               AM2=item["AM2"],
                               AM3=item["AM3"],
                               AM4=item["AM4"],
                               AM5=item["AM5"],
                               FM1=item["FM1"],
                               FM2=item["FM2"],
                               FM3=item["FM3"],
                               FM4=item["FM4"],
                               FM5=item["FM5"],
                               )
            records.append(record)
        self.db.add_all(records)
        self.db.commit()
        return records

    def get_records_by_reqIds(self, reqIds: []) -> TCellPack:
        """
        通过请求ID列表查询记录
        """
        records = self.db.query(TCellPack).filter(and_(TCellPack.reqId.in_(reqIds))).all()
        if records:
            return records
        return None

    def get_record_latest_by_id(self, dev, reqid: str) -> TCellPack:
        """
        根据设备ID和请求ID，查询记录
        """
        record = self.db.query(TCellPack).filter(
            and_(TCellPack.reqId == reqid,
                 TCellPack.did == dev)).order_by(desc(TCellPack.ts)).first()
        if record:
            return record
        return None

    def get_records_latest_by_reqIds(self, devs: [], reqIds: []) -> TCellPack:
        """
        根据设备ID列表和请求ID列表，查询记录
        """
        items = []
        for reqId in reqIds:
            for dev in devs:
                record = self.get_record_latest_by_id(dev, reqId)
                if record:
                    items.append(record)
        if len(items) == 0:
            return None
        return items

    def get_records_by_limit(self, dids, limit) -> TCellPack:
        """
        根据设备ID列表和limit，查询记录
        """
        items = []
        for did in dids:
            item = self.db.query(TCellPack).filter(TCellPack.did == did) \
                .order_by(desc(TCellPack.ts)).limit(limit).all()
            if item:
                items.append(item)
        if len(items) == 0:
            return None
        return items

    def delete_record(self, reqid):
        """
        根据请求ID删除记录
        """
        self.db.query(TCellPack).filter(TCellPack.reqId == reqid).delete()
        self.db.commit()
