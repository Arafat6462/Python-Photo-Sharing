# Photo Sharing App Enhancement Plan

This document outlines the plan to enhance the Django Photo Sharing application. The goal is to add new features while maintaining the existing monolithic architecture, as requested.

---

### Phase 1: Implement Core Models & Views

**Objective:** Extend the data structure and create the necessary pages to support new features like comments, ratings, and additional photo metadata.

1.  **Refine Data Models (`photos/models.py`):**
    *   Update the `Photo` model to add:
        *   `caption`: `models.TextField()`
        *   `location`: `models.CharField(max_length=100)`
        *   `people_present`: `models.CharField(max_length=255)`
    *   Create a new `Comment` model:
        *   `photo`: `models.ForeignKey(Photo, ...)`
        *   `user`: `models.ForeignKey(User, ...)`
        *   `text`: `models.TextField()`
        *   `created_at`: `models.DateTimeField(auto_now_add=True)`
    *   Create a new `Rating` model:
        *   `photo`: `models.ForeignKey(Photo, ...)`
        *   `user`: `models.ForeignKey(User, ...)`
        *   `score`: `models.IntegerField()` (e.g., 1-5)

2.  **Apply Database Changes:**
    *   Run `python manage.py makemigrations photos`.
    *   Run `python manage.py migrate`.

3.  **Update Creator Onboarding & Uploads:**
    *   Confirm the `is_creator` checkbox on the signup form works as intended.
    *   Update the photo upload form in `photos/forms.py` and the template in `photos/templates/upload_photo.html` to include the new metadata fields (`caption`, `location`, `people_present`).

4.  **Create Photo Detail Page:**
    *   Create a new view in `photos/views.py` to handle displaying a single photo and its details.
    *   Create a new template `photos/templates/photo_detail.html`.
    *   This template will display the photo, its metadata, the average rating, a list of comments, and forms for adding a new comment and a rating.
    *   Add a new URL pattern in `photos/urls.py` to link to this detail view (e.g., `/photo/<int:photo_id>/`).

---

### Phase 2: Add Dynamic Interactions with JavaScript (AJAX)

**Objective:** Improve user experience by allowing users to comment and rate photos without requiring a full page reload.

1.  **Dynamic Commenting:**
    *   Create a new view in `photos/views.py` that accepts a `POST` request with a photo ID and comment text. This view will save the comment and return a JSON response.
    *   Add a new URL for this view.
    *   In the `photo_detail.html` template, add a JavaScript snippet that uses the `fetch` API to send the comment form data to the new view and dynamically appends the new comment to the comment list on success.

2.  **Dynamic Ratings:**
    *   Create a new view that accepts a `POST` request with a photo ID and a rating score. This view will save the rating and return the new average score as a JSON response.
    *   Add a new URL for this view.
    *   In `photo_detail.html`, add JavaScript to send the rating to the view and update the displayed average rating on success.

---

### Phase 3: Scalability & Performance

**Objective:** Introduce basic scalability measures appropriate for a cloud-hosted application.

1.  **Azure CDN for Media:**
    *   Configure an Azure CDN endpoint and point it to the Azure Blob Storage container where media files are stored.
    *   Update the `MEDIA_URL` in `photoshare/deployment.py` to use the CDN URL in production.

2.  **Django View Caching:**
    *   Implement server-side caching for the main `gallery` view to reduce database queries for repeat visitors. This can be done using Django's built-in caching framework.
