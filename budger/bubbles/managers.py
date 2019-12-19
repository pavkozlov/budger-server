from django.db import models
from budger.directory.models.entity import Entity, EntityGroup


INSPECTION_1 = 282
INSPECTION_2 = 283
INSPECTION_3 = 284
INSPECTION_4 = 285
INSPECTION_5 = 286
INSPECTION_6 = 287


class EntityBubbleManager(models.Manager):

    ogrn = {
        INSPECTION_1: ["1025002870837", "1027739562256"],

        INSPECTION_2: ["1105001005340", "1075024000248", "1067746507344", "1035009553259", "1035000704749",
                       "1035005501431", "1035005000117", "1057748113961", "1045022400070", "1115024000552",
                       "1035008250474"],

        INSPECTION_3: ["1025005245055", "1185053043174", "1125012008021", "1025002042009", "1125024004918",
                       "1035004463230", "1125024004467"],

        INSPECTION_4: ["1125024004973", "1135024006776", "1185053037476", "1095024003910", "1125024005920",
                       "1027700546510", "1137799018081", "1045003352261", "1037739442707"],

        INSPECTION_5: ["1027739119121", "1035009552654", "1025002870837", "1145040006517", "1025001766096",
                       "1135024007887", "1125047013772", "1115024008868", "1037739557020"],

        INSPECTION_6: ["1027700524037", "1027739809460", "1125024004709", "1035000700668", "1037700160222",
                       "1037719012407", "1125047008569", "1135024006831", "1165024054161", "1195053001747",
                       "1125024000287"]
    }

    def get_entities_by_inspection(self, department_id):

        def _get_id_list(ogrn_list):
            return list(Entity.objects.filter(ogrn__in=ogrn_list).values_list('id', flat=True))

        if department_id in self.ogrn:
            entities_id = _get_id_list(self.ogrn[department_id])

            if department_id == self.INSPECTION_5:
                entities_id += EntityGroup.objects.get(code='municipals').data

            return super(EntityBubbleManager, self).get_queryset().filter(entity_id__in=entities_id)

        return super(EntityBubbleManager, self).none()
