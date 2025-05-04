from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup as BSoup
from news.models import Headline
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

def scrape(request, name):
    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    category_urls = {
        "sports": "https://www.espn.com/",
        "entertainment": "https://www.buzzfeed.com/entertainment",
        "politics": "https://www.politico.com/",
        "opinion": "https://www.nytimes.com/section/opinion",
        "breaking-news": "https://www.cnn.com/world",
        "technology": "https://www.theverge.com/tech",
        "health": "https://www.webmd.com/news",
    }
    url = category_urls.get(name)
    if not url:
        logger.error(f"Invalid category: {name}")
        return JsonResponse({"error": f"Invalid category: {name}"}, status=400)

    try:
        response = session.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to fetch articles for category {name}. Status code: {response.status_code}")
            return JsonResponse({"error": f"Failed to fetch articles. Status code: {response.status_code}"}, status=500)

        soup = BSoup(response.content, "html.parser")
        articles = soup.find_all("article")

        if not articles:
            logger.warning(f"No articles found for category {name}.")
            return JsonResponse({"error": f"No articles found for category {name}."}, status=404)

        for article in articles:
            try:
                link_tag = article.find("a", href=True)
                title_tag = article.find("h2")
                img_tag = article.find("img")

                if link_tag and title_tag:
                    link = link_tag["href"]
                    title = title_tag.text.strip()

                    # Handle different attributes for image URLs
                    image = ""
                    if img_tag:
                        image = img_tag.get("src") or img_tag.get("data-src") or img_tag.get("srcset", "").split(" ")[0]

                    # Fallback to placeholder image if no valid image URL is found
                    if not image:
                        image = "https://via.placeholder.com/150"

                    # Save the article to the database
                    Headline.objects.get_or_create(title=title, url=link, image=image)
            except Exception as e:
                logger.error(f"Error processing an article for category {name}: {e}")

    except Exception as e:
        logger.error(f"Error in scrape function for category {name}: {e}")
        return JsonResponse({"error": str(e)}, status=500)

    return redirect("../")

def search_articles(request):
    query = request.GET.get("q", "").lower()
    articles = Headline.objects.filter(title__icontains=query)  # Query using title__icontains
    results = [
        {"title": article.title, "url": article.url, "image": article.image}
        for article in articles
    ]
    return JsonResponse({"results": results})

def news_list(request):
    headlines = Headline.objects.all()[::-1]  # Retrieve all articles in reverse order
    context = {"object_list": headlines}
    return render(request, "news/home.html", context)
