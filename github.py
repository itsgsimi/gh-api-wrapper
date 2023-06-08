from fastapi import HTTPException, Depends, Header, APIRouter
import logging
import httpx
import os
from cache import cached_with_dependency, CACHE
from util import extract_next_page_url
from config import GITHUB_API_URL

gh_router = APIRouter(prefix="/api/github", tags=["Github API"])  # Set the prefix for the router

def get_github_client():
    return httpx.AsyncClient(headers={"Accept": "application/vnd.github.v3+json"})

@gh_router.get("/repo/{org_name}/{repo_name}", tags=["Github API"])
@cached_with_dependency(CACHE)
async def get_repo(org_name: str, repo_name: str, token: str = Header(...), client: httpx.AsyncClient = Depends(get_github_client)):
    try:
        full_repo_name = f"{org_name}/{repo_name}"
        response = await client.get(
            f"{GITHUB_API_URL}/repos/{full_repo_name}", headers={"Authorization": f"token {token}"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error occurred: {e}")
        raise e

@gh_router.get("/search_file/{org_name}/{file_name}/{search_text}", tags=["Github API"])
@cached_with_dependency(CACHE)
async def search_repos(org_name: str, file_name: str, 
                       search_text: str, 
                       page: int = 1, 
                       per_page: int = 100, 
                       token: str = Header(...), 
                       client: httpx.AsyncClient = Depends(get_github_client)):
    try:
        search_params = {
            "q": f"org:{org_name} filename:{file_name} in:file {search_text}",
            "page": page,
            "per_page": per_page
        }

        all_repo_names = []

        while True:
            response = await client.get(
                f"{GITHUB_API_URL}/search/code",
                params=search_params,
                headers={"Authorization": f"token {token}"}
            )
            response.raise_for_status()
            search_results = response.json()

            repo_names = [item["repository"]["full_name"] for item in search_results.get("items", [])]
            all_repo_names.extend(repo_names)

            # Check if there are more pages
            link_header = response.headers.get("Link")
            if link_header and "rel=\"next\"" in link_header:
                # Extract the URL for the next page
                next_page_url = extract_next_page_url(link_header)
                if next_page_url:
                    # Update the search URL and continue to the next page
                    search_url = next_page_url
                    page += 1
                    search_params["page"] = page
                else:
                    # Break the loop if the next page URL couldn't be extracted
                    break
            else:
                # Break the loop if there are no more pages
                break

        return {"repositories": all_repo_names}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="GitHub API request failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")