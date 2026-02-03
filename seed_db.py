import os
import django
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from qbank.models import Subject, SubTopic, Chapter, Question, Option
from content.models import Banner, Testimonial, BookCategory, Book, Drug
from store.models import SubscriptionPlan, CoinPackage

def seed_data():
    print("Seeding database...")

    # 1. Banners
    Banner.objects.get_or_create(
        title="Invite Friends & Earn Big!",
        description="You get 100 Coins + 10% Cash Commission. Your friend gets 50 Coins.",
        image_url="https://placeholder.com/banner1.png",
        is_active=True
    )

    # 2. Testimonials
    Testimonial.objects.get_or_create(
        user_name="Dr. Rajesh Kumar",
        user_role="BVSc, MVSc",
        content="VetPathshala helped me pass my exams with flying colors. The Q Bank and lectures were incredibly helpful for my preparation."
    )

    # 3. Question Bank Hierarchy
    subject, _ = Subject.objects.get_or_create(
        title_en="General Hindi",
        title_hi="सामान्य हिंदी",
        description="General Hindi covers grammar, vocabulary, and comprehension skills.",
        icon_identifier="BookA",
        order=1
    )

    subtopic, _ = SubTopic.objects.get_or_create(
        subject=subject,
        title="Noun, Pronoun, Verb, Adjective",
        description="The key parts of speech that form the foundation of language.",
        order=1
    )

    chapter, _ = Chapter.objects.get_or_create(
        sub_topic=subtopic,
        title="Noun",
        description="A noun is a word that names a person, place, thing, or idea.",
        order=1
    )

    # 4. Questions
    q1, created = Question.objects.get_or_create(
        chapter=chapter,
        text="मेरा भाई इतना ............ है कि सामान कहीं भी रखकर भूल जाता है। इस रिक्त स्थान के लिए सही भाववाचक संज्ञा वाला विकल्प चुनें:",
        is_pyq=True,
        pyq_info="S.S.C. G.D. EXAM (2024)",
        difficulty="Medium"
    )

    if created:
        Option.objects.create(question=q1, text="बेकार", identifier="A", is_correct=False)
        Option.objects.create(question=q1, text="भुलक्कड़", identifier="B", is_correct=True)
        Option.objects.create(question=q1, text="लुटेरा", identifier="C", is_correct=False)
        Option.objects.create(question=q1, text="बुद्ध", identifier="D", is_correct=False)

    # 5. Ebooks
    cat, _ = BookCategory.objects.get_or_create(name="Abdul Kalam", color_code="#1e293b")
    Book.objects.get_or_create(
        category=cat,
        title="Dark Desire",
        author="Vivek Shukla",
        description="A gripping tale of mystery.",
        rating=4.5,
        price=0.00,
        is_premium=False
    )

    # 6. Store
    SubscriptionPlan.objects.get_or_create(
        title="Mission Patwari 2025-2026",
        description="Full Test Series + PYP + Mock",
        base_price=1999,
        discount_percentage=67,
        duration_months=3,
        features=["Tests", "PY Papers", "Mock Tests"]
    )

    CoinPackage.objects.get_or_create(
        coins_amount=100,
        price=50,
        original_price=500
    )

    print("Seeding complete!")

if __name__ == "__main__":
    seed_data()
