from datetime import timedelta
from django.utils import timezone

from apps.base.functions import uidGenerator


users_data = [
    {
        "model": "users.User",
        "pk": 2,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "med.ali@ed.gov",
            "first_name": "Med",
            "last_name": "Ali",
            "phone_number": "77281452",
            "is_verified": True,
            "password": "med.ali"
        }
    },
    {
        "model": "users.User",
        "pk": 3,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "zeinab.ousleyeh@geocities.com",
            "first_name": "Zeinab",
            "last_name": "Ousleyeh",
            "phone_number": "77062465",
            "is_verified": True,
            "password": "zeinab.ousleyeh"
        }
    },
    {
        "model": "users.User",
        "pk": 4,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "avaleh.omar@washington.edu",
            "first_name": "Avaleh",
            "last_name": "Omar",
            "phone_number": "77352465",
            "is_verified": True,
            "password": "avaleh.omar"
        }
    },
    {
        "model": "users.User",
        "pk": 5,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "ibrahim.anas@geocities.com",
            "first_name": "Ibrahim",
            "last_name": "Anas",
            "phone_number": "77752485",
            "is_verified": True,
            "password": "ibrahim.anas"
        }
    },
    {
        "model": "users.User",
        "pk": 6,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "Saad.ahmed@geocities.com",
            "first_name": "Saad",
            "last_name": "Ahmed",
            "phone_number": "77652465",
            "is_verified": True,
            "password": "Saad.ahmed"
        }
    },
    {
        "model": "users.User",
        "pk": 7,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "hamze.idriss@geocities.com",
            "first_name": "Hamze",
            "last_name": "Idriss",
            "phone_number": "77752465",
            "is_verified": True,
            "password": "hamze.idriss"
        }
    },
    {
        "model": "users.User",
        "pk": 8,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "charco.abdi@geocities.com",
            "first_name": "Charco",
            "last_name": "Abdi",
            "phone_number": "77130292",
            "is_verified": True,
            "password": "charco.abdi"
        }
    },
    {
        "model": "users.User",
        "pk": 9,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "hassan.abdi@timesonline.co.uk",
            "first_name": "Hassan",
            "last_name": "Abdi",
            "phone_number": "77864532",
            "is_verified": True,
            "password": "hassan.abdi"
        }
    },
    {
        "model": "users.User",
        "pk": 10,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "email": "nazmul.ahmed@geocities.com",
            "first_name": "Nazmul",
            "last_name": "Ahmed",
            "phone_number": "77022465",
            "is_verified": True,
            "password": "nazmul.ahmed"
        }
    }
]


categories_data = [
    {
        "model": "product.Category",
        "pk": 1,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "produits laitiers",
            "slug": "produits-laitiers",
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
    },
    {
        "model": "product.Category",
        "pk": 2,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits surgelés",
            "slug": "produits-surgeles",
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
    },
    {
        "model": "product.Category",
        "pk": 3,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits secs",
            "slug": "produits-secs",
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
    },
    {
        "model": "product.Category",
        "pk": 4,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits d'épicerie",
            "slug": "produits-epicerie",
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
    },
    {
        "model": "product.Category",
        "pk": 5,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Boissons",
            "slug": "boissons",
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
    },
    {
        "model": "product.Category",
        "pk": 6,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits d'hygiène et de beauté",
            "slug": "produits-hygiene-et-beautee",
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
    },
    {
        "model": "product.Category",
        "pk": 7,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits pour bébés",
            "slug": "produits-pour-bebes",
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
    },
    {
        "model": "product.Category",
        "pk": 8,
        "fields": {
            "public_id": f"{uidGenerator()}",
            "name": "Produits ménagers",
            "slug": "produits-menagers",
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
    }
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
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
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
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
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
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
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
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
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
            "created_at": str(timezone.now()),
            "updated_at": str(timezone.now()),
        }
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
            "created_at": str(timezone.now() + timedelta(days=-1) + timedelta(hours=1)),
            "updated_at": str(timezone.now()),
        }
    },
]
