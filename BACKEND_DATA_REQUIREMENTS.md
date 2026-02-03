# Backend Data Requirements & Design
This document outlines the dynamic data requirements for the VetPathshala application based on the frontend architecture. It serves as a blueprint for the backend database models and API endpoints.

## 1. Authentication & User Profile
**Goal:** Manage user identity, roles, and global settings.

### Data Models
*   **User**:
    *   `username`, `email`, `password_hash`
    *   `phone_number` (verified via OTP)
    *   `role` (Enum: 'Student', 'Doctor', etc.)
    *   `language_preference` (Enum: 'en', 'hi')
    *   `created_at`, `last_login`
*   **Wallet/Profile**:
    *   `user_id` (FK)
    *   `coin_balance` (Integer, Default: 0)
    *   `is_premium` (Boolean) - *Derived from active subscriptions usually*

### API Endpoints Needed
*   `POST /api/auth/register`
*   `POST /api/auth/login`
*   `POST /api/auth/verify-otp`
*   `GET /api/user/profile` (Returns balance, role, name, etc.)
*   `PATCH /api/user/settings` (Update language, etc.)

---

## 2. Dashboard
**Goal:** Provide a central hub with dynamic content, progress summaries, and marketing elements.

### Data Models
*   **Banner**:
    *   `title`, `description`, `reward_text`
    *   `image_url`
    *   `action_link` (Where it navigates to)
    *   `is_active`
*   **Testimonial (Success Stories)**:
    *   `user_name`, `user_role` (degrees)
    *   `content` (The review text)
    *   `avatar_url`
*   **RecentActivity** (Virtual/Aggregated):
    *   Calculated real-time from UserProgress.

### API Endpoints Needed
*   `GET /api/dashboard/home`
    *   Returns: `{ banners: [], testimonials: [], recent_activity: [], categories: [] }`

---

## 3. Education / Question Bank (Core Feature)
**Goal:** Hierarchical study material with tracking.

### Data Models
*   **Subject (Topic)**:
    *   `title` (Translatable: en/hi)
    *   `description`
    *   `icon_identifier` (String for frontend mapping)
    *   `order`
*   **SubTopic**:
    *   `subject_id` (FK)
    *   `title`, `description`
    *   `order`
*   **Chapter**:
    *   `sub_topic_id` (FK)
    *   `title`, `description`
    *   `order`
*   **Question**:
    *   `chapter_id` (FK)
    *   `text` (Rich text/HTML support likely needed)
    *   `type` (MCQ, True/False)
    *   `is_pyq` (Boolean), `pyq_info` (Text: "SSC 2024 Exam")
    *   `difficulty`, `tags`
*   **Option**:
    *   `question_id` (FK)
    *   `text`, `identifier` (A, B, C, D)
    *   `is_correct` (Boolean)
*   **UserProgress**:
    *   `user_id`, `chapter_id`/`sub_topic_id`
    *   `questions_attempted`, `questions_correct`
    *   `last_accessed`
*   **QuestionInteraction**:
    *   `user_id`, `question_id`
    *   `is_bookmarked`
    *   `user_note` (Text)
    *   `is_liked`, `is_reported`

### API Endpoints Needed
*   `GET /api/qbank/subjects` (Includes progress % per subject)
*   `GET /api/qbank/subjects/{id}/subtopics`
*   `GET /api/qbank/subtopics/{id}/chapters`
*   `GET /api/qbank/chapters/{id}/questions`
    *   Supports filters: `is_bookmarked=true`, `is_pyq=true`
*   `POST /api/qbank/questions/{id}/submit`
    *   Records attempt, updates progress.
*   `POST /api/qbank/questions/{id}/toggle-bookmark`

---

## 4. Ebooks & Library
**Goal:** Digital library with free and premium content.

### Data Models
*   **BookCategory** (Subjects):
    *   `name`, `color_code`
*   **Book**:
    *   `category_id` (FK)
    *   `title`, `author`
    *   `cover_image_url`, `cover_color`
    *   `description`
    *   `price` (Decimal, 0 = Free)
    *   `is_premium` (Boolean)
    *   `rating` (Float, 1-5)
    *   `pdf_url` (Protected resource)

### API Endpoints Needed
*   `GET /api/ebooks/categories`
*   `GET /api/ebooks/books` (Filters: `featured`, `trending`, `popular`, `search`)
*   `GET /api/ebooks/books/{id}`

---

## 5. Drug Center
**Goal:** Reference guide and tools for veterinary drugs.

### Data Models
*   **Drug**:
    *   `name`
    *   `composition`, `dosage`, `indications`
    *   `contraindications`, `side_effects`
    *   `category` (Antibiotic, NSAID, etc.)

### API Endpoints Needed
*   `GET /api/drugs` (Searchable)
*   `GET /api/drugs/{id}`

---

## 6. Commerce (Store & Subscription)
**Goal:** Monetization via coins and subscriptions.

### Data Models
*   **SubscriptionPlan**:
    *   `title`, `description`
    *   `base_price`, `discount_percentage`
    *   `duration_months`
    *   `features` (JSON list of strings)
*   **CoinPackage**:
    *   `coins_amount`
    *   `price`, `original_price`
*   **Transaction**:
    *   `user_id`
    *   `amount`, `currency`
    *   `type` (COIN_PURCHASE, SUB_PURCHASE, EBOOK_BUY)
    *   `status` (PENDING, SUCCESS, FAILED)
*   **UserSubscription**:
    *   `user_id`, `plan_id`
    *   `start_date`, `end_date`
    *   `is_active`

### API Endpoints Needed
*   `GET /api/store/coin-packages`
*   `GET /api/store/plans`
*   `POST /api/store/purchase` (Initiate payment gateway)
*   `GET /api/user/subscriptions`

---

## Summary of Backend Tech Stack Recommendation
*   **Framework**: Django / Django REST Framework (DRF)
*   **Database**: PostgreSQL
*   **Storage**: AWS S3 (for Ebooks, Banners, Avatars)
*   **Auth**: JWT (Simple JWT)
