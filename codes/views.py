from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import ResponseCode, SavedList
import re, requests


def home(request):
    return render(request, "home.html")


def signup_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("search")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("search")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def search_codes(request):
    query = request.GET.get("filter", "").strip()  # User's filter input
    codes = []  # Store fetched code details
    saved_message = ""  # Feedback message for saved lists

    if query:
        # Regex-like filtering
        if "x" in query:
            pattern = query.replace("x", r"\d")
            possible_codes = [str(code) for code in range(100, 600)]
            for code in possible_codes:
                if re.match(f"^{pattern}$", code):
                    codes.append(fetch_http_dog_data(code))
        else:
            codes.append(fetch_http_dog_data(query))

    codes = [code for code in codes if code]  # Remove None entries

    # Handle POST request for saving the list
    if request.method == "POST":
        list_name = request.POST.get("list_name", "").strip()  # Get list name
        selected_codes = request.POST.getlist("selected_codes")  # Selected code IDs

        if list_name and selected_codes:
            # Prepare JSON data for storage
            selected_data = [code for code in codes if code["code"] in selected_codes]
            SavedList.objects.create(
                user=request.user, name=list_name, codes=selected_data
            )
            saved_message = "List saved successfully!"

    return render(
        request,
        "search.html",
        {"codes": codes, "query": query, "saved_message": saved_message},
    )


def fetch_http_dog_data(code):
    """
    Fetch details for a specific HTTP response code from https://http.dog/{code}.json
    """
    url = f"https://http.dog/{code}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "code": str(data["status_code"]),
                "title": data["title"],
                "image_url": data["image"]["jpg"],
                "learn_more_url": data["url"],
            }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for code {code}: {e}")
    return None


@login_required
def view_saved_lists(request):
    saved_lists = SavedList.objects.filter(user=request.user).order_by("-creation_date")
    return render(request, "saved_lists.html", {"saved_lists": saved_lists})


def saved_list_detail(request, list_id):
    # Retrieve the saved list by its ID
    saved_list = get_object_or_404(SavedList, id=list_id)

    # Pass the saved list details to the template
    return render(request, "saved_list_detail.html", {"saved_list": saved_list})


@login_required
def delete_list(request, list_id):
    saved_list = SavedList.objects.get(id=list_id, user=request.user)
    saved_list.delete()
    return redirect("saved_lists")


@login_required
def edit_list(request, list_id):
    # Get the saved list by ID and ensure it's the logged-in user's list
    saved_list = get_object_or_404(SavedList, id=list_id, user=request.user)

    # Get the current codes from the SavedList
    saved_list_codes = [code["code"] for code in saved_list.codes]

    if request.method == "POST":
        # Get selected codes from the form (checkboxes)
        selected_codes = request.POST.getlist("selected_codes")

        # Fetch data for selected codes
        selected_data = [
            fetch_http_dog_data(code)
            for code in selected_codes
            if fetch_http_dog_data(code)
        ]

        # Update the saved list with new selected codes
        saved_list.codes = selected_data
        saved_list.save()

        return redirect("saved_list_detail", list_id=saved_list.id)

    # Fetch all possible response codes for selection
    codes = ResponseCode.objects.all()

    return render(
        request,
        "edit_list.html",
        {
            "saved_list": saved_list,
            "codes": codes,
            "saved_list_codes": saved_list_codes,  # List of already selected codes
        },
    )
