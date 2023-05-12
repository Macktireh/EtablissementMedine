from datetime import timedelta
from random import randint

from django.utils import timezone
from faker import Faker

from apps.core.utils import uidGenerator


fake = Faker(locale="fr_FR")

_users_data = []

list_email_unique = [fake.unique.email() for _ in range(11, 101)]
list_phone_number_unique = [fake.unique.phone_number() for _ in range(11, 101)]

for i, email in enumerate(list_email_unique):
    password = email.split("@")[0]
    _users_data.append(
        {
            "model": "authUser.User",
            "pk": i + 11,
            "fields": {
                "public_id": f"{uidGenerator()}",
                "email": f"{email}",
                "name": f"{fake.name()}",
                "phone_number": f"+253{randint(100000, 1000000)}",
                # "phone_number": f"{list_phone_number_unique[i]}",
                "verified": True,
                "password": f"{password}",
            },
        }
    )


users_data = [
    {
        "model": "authUser.User",
        "pk": 2,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "med.ali@ed.gov",
            "name": "Med Ali",
            "phone_number": "+25377281452",
            "verified": True,
            "password": "med.ali",
        },
    },
    {
        "model": "authUser.User",
        "pk": 3,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "zeinab.ousleyeh@geocities.com",
            "name": "Zeinab Ousleyeh",
            "phone_number": "+25377062465",
            "verified": True,
            "password": "zeinab.ousleyeh",
        },
    },
    {
        "model": "authUser.User",
        "pk": 4,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "avaleh.omar@washington.edu",
            "name": "Avaleh Omar",
            "phone_number": "+25377352465",
            "verified": True,
            "password": "avaleh.omar",
        },
    },
    {
        "model": "authUser.User",
        "pk": 5,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "ibrahim.anas@geocities.com",
            "name": "Ibrahim Anas",
            "phone_number": "+25377752485",
            "verified": True,
            "password": "ibrahim.anas",
        },
    },
    {
        "model": "authUser.User",
        "pk": 6,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "Saad.ahmed@geocities.com",
            "name": "Saad Ahmed",
            "phone_number": "+25377652465",
            "verified": True,
            "password": "Saad.ahmed",
        },
    },
    {
        "model": "authUser.User",
        "pk": 7,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "hamze.idriss@geocities.com",
            "name": "Hamze Idriss",
            "phone_number": "+25377752465",
            "verified": True,
            "password": "hamze.idriss",
        },
    },
    {
        "model": "authUser.User",
        "pk": 8,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "charco.abdi@geocities.com",
            "name": "Charco Abdi",
            "phone_number": "+25377130292",
            "verified": True,
            "password": "charco.abdi",
        },
    },
    {
        "model": "authUser.User",
        "pk": 9,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "hassan.abdi@timesonline.co.uk",
            "name": "Hassan Abdi",
            "phone_number": "+25377864532",
            "verified": True,
            "password": "hassan.abdi",
        },
    },
    {
        "model": "authUser.User",
        "pk": 10,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "nazmul.ahmed@geocities.com",
            "name": "Nazmul Ahmed",
            "phone_number": "+25377022465",
            "verified": True,
            "password": "nazmul.ahmed",
        },
    },
] + _users_data

address_data = []

for i, _ in enumerate(users_data):
    address_data.append(
        {
            "model": "customer.Address",
            "pk": i + 2,
            "fields": {
                "user_id": f"{i + 2}",
                "street_address": f"{fake.street_address()}",
                "city": f"{fake.city()}",
                "zipcode": f"{fake.postcode()}",
                "country": f"{fake.current_country()}",
            },
        }
    )


categories_data = [
    {
        "model": "product.Category",
        "pk": 1,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "produits laitiers",
            "slug": "produits-laitiers",
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Category",
        "pk": 2,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits surgelés",
            "slug": "produits-surgeles",
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Category",
        "pk": 3,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits secs",
            "slug": "produits-secs",
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Category",
        "pk": 4,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits d'épicerie",
            "slug": "produits-epicerie",
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Category",
        "pk": 5,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Boissons",
            "slug": "boissons",
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Category",
        "pk": 6,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits d'hygiène et de beauté",
            "slug": "produits-hygiene-et-beautee",
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Category",
        "pk": 7,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits pour bébés",
            "slug": "produits-pour-bebes",
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Category",
        "pk": 8,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits ménagers",
            "slug": "produits-menagers",
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
]


products_data = [
    {
        "model": "product.Product",
        "pk": 1,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Yaourt nature",
            "slug": "yaourt-nature",
            "price": "120",
            "stock": 63,
            "description": "Le yaourt nature est un produit laitier fermenté à base de lait. Il est riche en calcium et en protéines, ce qui en fait un aliment nutritif pour les personnes de tous âges. Il peut être consommé tel quel ou mélangé avec des fruits ou du miel pour un goût sucré.",
            "category": 1,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 2,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Fromage bleu",
            "slug": "fromage-bleu",
            "price": "80",
            "stock": 53,
            "description": "Le fromage bleu est un fromage à pâte persillée fabriqué à partir de lait de vache, de brebis ou de chèvre. Il a une texture crémeuse et un goût fort et salé. Il est souvent utilisé pour ajouter de la saveur à des salades, des pâtes ou des sandwichs.",
            "category": 1,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 3,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Lait de soja",
            "slug": "lait-de-soja",
            "price": "160",
            "stock": 63,
            "description": "Le lait de soja est une alternative végétale au lait de vache. Il est fabriqué à partir de graines de soja broyées et mélangées avec de l'eau. Il est riche en protéines et en nutriments essentiels, mais ne contient pas de lactose. Il est souvent utilisé par les personnes allergiques au lait ou par celles qui suivent un régime végétalien ou végétarien.",
            "category": 1,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 4,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Pizza surgelée",
            "slug": "pizza-surgelee",
            "price": "150",
            "stock": 23,
            "description": "La pizza surgelée est une option pratique pour les repas rapides. Elle est généralement composée d'une croûte, de sauce tomate et de fromage, avec une variété de garnitures disponibles telles que le pepperoni, les légumes ou le poulet. Elle peut être cuite au four en quelques minutes et servie chaude.",
            "category": 2,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 5,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Poisson surgelé",
            "slug": "poisson-surgelee",
            "price": "120",
            "stock": 26,
            "description": "Le poisson surgelé est une alternative pratique et économique au poisson frais. Il est généralement emballé individuellement et peut être cuit directement à partir du congélateur. Les variétés courantes comprennent le saumon, la morue, le tilapia et le cabillaud.",
            "category": 2,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 6,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Légumes surgelés",
            "slug": "legumes-surgelees",
            "price": "100",
            "stock": 43,
            "description": "Les légumes surgelés sont une option pratique pour les repas rapides ou pour ceux qui ne peuvent pas acheter de légumes frais régulièrement. Ils sont emballés individuellement ou mélangés dans des sacs et peuvent être cuits rapidement au micro-ondes ou à la vapeur. Les variétés courantes comprennent les pois, les carottes, le brocoli et les haricots verts.",
            "category": 2,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 7,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Noix de cajou grillées",
            "slug": "noix-de-cajou-grillees",
            "price": "130",
            "stock": 123,
            "description": "Ces noix de cajou sont légèrement grillées pour leur donner une saveur croustillante et délicieuse. Elles sont riches en protéines et en graisses saines, ce qui en fait une collation saine et satisfaisante. Les noix de cajou grillées sont également un excellent ajout aux salades et aux plats cuisinés.",
            "category": 3,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 8,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Riz basmati biologique",
            "slug": "riz-basmati-biologique",
            "price": "70",
            "stock": 210,
            "description": "Le riz basmati biologique est un choix parfait pour les personnes soucieuses de leur santé et de l'environnement. Ce riz est cultivé sans l'utilisation de produits chimiques nocifs, ce qui en fait une option plus saine que le riz traditionnel. Le riz basmati a une texture légère et un goût subtil, ce qui le rend parfait pour accompagner les plats épicés.",
            "category": 3,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 9,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Pâtes de lentilles rouges",
            "slug": "pates-de-lentilles-rouges",
            "price": "60",
            "stock": 200,
            "description": "Ces pâtes de lentilles rouges sont une alternative saine aux pâtes traditionnelles à base de blé. Elles sont riches en protéines et en fibres, ce qui en fait un choix idéal pour les végétariens et les personnes soucieuses de leur santé. Les pâtes de lentilles rouges ont une texture ferme et une saveur légèrement sucrée, ce qui les rend parfaites pour les sauces légères ou pour les mélanger avec des légumes frais.",
            "category": 3,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 10,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Huile d'olive extra vierge",
            "slug": "huile-d-olive-extra-vierge",
            "price": "110",
            "stock": 200,
            "description": "L'huile d'olive extra vierge est une huile de cuisine saine et délicieuse qui est souvent utilisée dans la cuisine méditerranéenne. Elle est riche en graisses monoinsaturées et est également une source de vitamine E.",
            "category": 4,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 11,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Sucre",
            "slug": "sucre",
            "price": "50",
            "stock": 250,
            "description": "Le sucre est un édulcorant courant qui est utilisé dans de nombreux produits alimentaires. Il peut être utilisé dans la cuisine pour sucrer les boissons chaudes, les desserts et les plats principaux.",
            "category": 4,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 12,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Farine",
            "slug": "farine",
            "price": "90",
            "stock": 200,
            "description": "La farine est un ingrédient de base utilisé pour faire du pain, des pâtisseries et des pâtes fraîches. Il existe de nombreuses variétés de farine, notamment la farine de blé, la farine d'épeautre et la farine de seigle.",
            "category": 4,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 13,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Eau minérale naturelle",
            "slug": "eau-minerale-naturelle",
            "price": "100",
            "stock": 300,
            "description": "Une eau pure et naturelle qui est extraite de sources souterraines et qui contient des minéraux essentiels pour une hydratation saine.",
            "category": 5,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 14,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Boisson énergisante",
            "slug": "boisson-energisante",
            "price": "110",
            "stock": 200,
            "description": "Une boisson qui contient de la caféine et des vitamines B pour une stimulation mentale et physique, généralement consommée avant une activité sportive ou une journée chargée.",
            "category": 5,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 15,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Sirop d'érable",
            "slug": "sirop-d-erable",
            "price": "90",
            "stock": 200,
            "description": "Un édulcorant naturel produit à partir de l'eau d'érable, ajoutant une saveur sucrée et délicieuse aux boissons chaudes telles que le café ou le thé.",
            "category": 5,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 16,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Dentifrice blanchissant",
            "slug": "dentifrice-blanchissant",
            "price": "80",
            "stock": 200,
            "description": "Ce dentifrice est spécialement formulé pour aider à éliminer les taches de surface et à blanchir les dents en douceur. Il contient des ingrédients actifs pour aider à renforcer l'émail et à prévenir les caries.",
            "category": 6,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 17,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Déodorant naturel",
            "slug": "deodorant-naturel",
            "price": "120",
            "stock": 200,
            "description": "Ce déodorant est formulé avec des ingrédients naturels pour aider à éliminer les odeurs tout en étant doux pour la peau. Il ne contient pas de produits chimiques agressifs et est sans parfum.",
            "category": 6,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 18,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Shampooing revitalisant",
            "slug": "shampooing-revitalisant",
            "price": "90",
            "stock": 200,
            "description": "Ce shampooing revitalisant est formulé pour nourrir les cheveux en profondeur et les laisser doux et soyeux. Il contient des ingrédients comme l'huile d'argan et le beurre de karité pour aider à réparer et renforcer les cheveux.",
            "category": 6,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 19,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Brosse à dents électrique",
            "slug": "brosse-a-dents-electrique",
            "price": "90",
            "stock": 200,
            "description": "Cette brosse à dents électrique est conçue pour nettoyer en profondeur les dents et les gencives tout en étant douce pour l'émail. Elle est équipée d'une tête de brosse interchangeable pour un nettoyage personnalisé.",
            "category": 6,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 20,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Biberons anti-coliques",
            "slug": "biberons-anti-coliques",
            "price": "90",
            "stock": 200,
            "description": "Les biberons anti-coliques sont spécialement conçus pour réduire l'ingestion d'air, ce qui peut aider à prévenir les coliques et les reflux.",
            "category": 7,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 21,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Couches jetables",
            "slug": "couches-jetables",
            "price": "90",
            "stock": 200,
            "description": "Les couches jetables sont pratiques et faciles à utiliser, et sont disponibles dans une variété de tailles pour s'adapter à la croissance de votre bébé.",
            "category": 7,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 22,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Tapis d'éveil",
            "slug": "tapis-d-eveil",
            "price": "130",
            "stock": 170,
            "description": "Un tapis d'éveil coloré et stimulant est parfait pour encourager le développement moteur et cognitif de votre bébé.",
            "category": 7,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 23,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Détergent à lessive",
            "slug": "detergent-a-lessive",
            "price": "40",
            "stock": 200,
            "description": "Un détergent à lessive efficace peut aider à éliminer la saleté et les taches des vêtements. Il existe des détergents en poudre, liquides ou en capsules, chacun offrant une formule différente pour répondre à vos besoins de lavage.",
            "category": 8,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 24,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Nettoyant multi-surfaces",
            "slug": "nettoyant-multi-surfaces",
            "price": "60",
            "stock": 200,
            "description": "Un nettoyant multi-surfaces est un produit polyvalent qui peut être utilisé pour nettoyer différents types de surfaces, y compris les comptoirs de cuisine, les planchers et les murs. Ils sont généralement disponibles sous forme de spray ou de lingettes.",
            "category": 8,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
    {
        "model": "product.Product",
        "pk": 25,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produit nettoyant pour vitres",
            "slug": "nettoyant-pour-vitres",
            "price": "90",
            "stock": 200,
            "description": "Un produit nettoyant pour vitres est un produit conçu pour éliminer les taches et les saletés des vitres sans laisser de traces. Ils sont généralement disponibles sous forme de spray ou de lingettes.",
            "category": 8,
            "created_at": str(
                timezone.now()
                + timedelta(days=randint(-200, 0))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
            "updated_at": str(
                timezone.now()
                + timedelta(days=randint(1, 200))
                + timedelta(hours=randint(-9, 9))
                + timedelta(minutes=randint(-20, 20))
                + timedelta(seconds=randint(-20, 20))
            ),
        },
    },
]


data = users_data + address_data + categories_data + products_data
