from django.core.management.base import BaseCommand
from users_app.models import CustomUser
from locations_app.models import Cemetery, Municipality
from locations_app.enums import CemeteryStatusEnum
from services_app.models import Service
from datetime import datetime


class Command(BaseCommand):
    help = 'Initialize database with initial data'

    def handle(self, *args, **options):
        municipality, created = Municipality.objects.get_or_create(name="Белгородский ГО")

        cemetery, created = Cemetery.objects.get_or_create(
            name="Ячнево",
            defaults={
                'coordinates': [[[50.63083552574989, 36.603673829704135], [50.63115879431887, 36.60436286527029],
                                 [50.63170479220884, 36.60709603630049], [50.63353112844288, 36.60840254578967],
                                 [50.634372576549886, 36.60891464383884], [50.63499194995814, 36.60929514760438],
                                 [50.636445172575755, 36.60895145064268], [50.636477155809864, 36.60896217947876],
                                 [50.636491228425946, 36.60886897271549], [50.63687163823348, 36.607645676102685],
                                 [50.63683070003533, 36.60754643436912], [50.63722415554296, 36.6063435179757],
                                 [50.637174262485445, 36.60627914495936], [50.639091977833495, 36.6005485791318],
                                 [50.63907321538832, 36.60053449753449], [50.63920438810992, 36.60015099142141],
                                 [50.63922315050247, 36.600168425780005], [50.64005145072704, 36.597709584266816],
                                 [50.63712442648206, 36.59270794402242], [50.637126132230314, 36.592599314557326],
                                 [50.636751221673954, 36.59258724461678], [50.63675652595659, 36.59226060320097],
                                 [50.636462431929395, 36.592264507958255], [50.63618694886871, 36.59209955210383],
                                 [50.6356163006903, 36.592089795885315], [50.63550371753611, 36.591995248017554],
                                 [50.63548978259513, 36.59181221028238], [50.6355166490623, 36.59169486363797],
                                 [50.635548632931645, 36.59166267712981], [50.63598851111679, 36.59167575428605],
                                 [50.63602134755759, 36.591622780658], [50.636031229421825, 36.58969491760855],
                                 [50.63604359638444, 36.58939652185563], [50.63241005438947, 36.58935550720561],
                                 [50.63233768760781, 36.59375648651238], [50.63144143967644, 36.59372300962612],
                                 [50.6314241722746, 36.594927625606736], [50.631065067101446, 36.594932990024766],
                                 [50.63097952013147, 36.594170722863325], [50.630836218222726, 36.593559179207936],
                                 [50.63062782614091, 36.59332768432213], [50.63049817107673, 36.59325526467872],
                                 [50.63021668187094, 36.593147976318114], [50.62974241137633, 36.59329013339592],
                                 [50.62964516827059, 36.5931640695722], [50.62905767026223, 36.593032641330474],
                                 [50.62932489822123, 36.59661226271331], [50.630012235856555, 36.596423738715366],
                                 [50.63010308068264, 36.59643446755145], [50.63016701428895, 36.596543164269626],
                                 [50.63030470005028, 36.597335111150066], [50.63033839348107, 36.5974417289584],
                                 [50.630395061335655, 36.5975294736346], [50.63047566947386, 36.597582447262646],
                                 [50.63142466781844, 36.59753937853018], [50.631496744414385, 36.597566200620335],
                                 [50.63154834948289, 36.59762856197994], [50.631687938200656, 36.598042663997205],
                                 [50.63176876944225, 36.59811603309298], [50.63185406654916, 36.5981562662282],
                                 [50.63232569230485, 36.59807373631022], [50.63220291107792, 36.59972845508263],
                                 [50.632925855176815, 36.60161638664331], [50.63215535602421, 36.60206582829698],
                                 [50.632116546109934, 36.602111425850254], [50.63210417810852, 36.60211410805927],
                                 [50.63179632944694, 36.60247760782999], [50.6317449845978, 36.602561402959424],
                                 [50.631616612093275, 36.602782014650906], [50.63135958472254, 36.60311401583997],
                                 [50.63095284627444, 36.6035729825476], [50.63083552574989, 36.603673829704135]]],
                'municipality': municipality,
                'date_start': datetime(2000, 1, 1),
                'date_end': datetime(2018, 1, 1),
                'description': 'Кладбище Ячнево',
                'status': CemeteryStatusEnum.CLOSED.name,
            }
        )

        services_data = [
            {'name': 'Заказ поминальной молитвы', 'price': 300.00,
             'description': 'Заказ поминальной молитвы Заказ панихиды в церкви на территории кладбища Ячнево. Срок исполнения не позднее 2-х дней с момента оплаты.'},
            {'name': 'Уборка места захоронения', 'price': 1000.00,
             'description': 'Проведем комплекс работ по уходу за захоронением. В услугу входит поиск места захоронения, уборка от снега или листвы и прочего мусора, вынос мусора с участка захоронения, очистка и протирка надмогильных сооружений специальными средствами, фотоотчет об оказанной услуге. Срок исполнения не позднее 2-х дней с момента оплаты.'},
            {'name': 'Возложение цветов', 'price': 800.00,
             'description': 'Возложим две гвоздики к месту захоронения Ваших близких. В услугу входит поиск места захоронения, возложение выбранных 2-х гвоздик, фотофиксация места захоронения (не менее четырех фотографий с различных ракурсов), фотоотчет об оказанной услуге. Срок исполнения не позднее 2-х дней с момента оплаты.',
             'is_multiple_price': True},
        ]
        for service_data in services_data:
            Service.objects.get_or_create(**service_data)

        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser('admin@admin.com', 'admin')

        self.stdout.write(self.style.SUCCESS('Database initialized successfully'))
