"""Search API routes — discover local businesses."""

from fastapi import APIRouter

from leadlocal.core.dependencies import CurrentUser, DBSession
from leadlocal.schemas.search import SearchRequest, SearchResponse
from leadlocal.services import search_service

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
async def search(req: SearchRequest, user: CurrentUser, db: DBSession):
    return await search_service.search_leads(db, user, req)
