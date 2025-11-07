import httpx
import os

SUBGRAPH_URL = os.getenv("PENDLE_SUBGRAPH_ARBITRUM", "https://api.thegraph.com/subgraphs/name/pendle/pendle-arbitrum-v2")

MARKETS_QUERY = """
query ($first:Int, $skip:Int) {
  markets(first:$first, skip:$skip) {
    id
    token0 { symbol id }
    token1 { symbol id }
    reserveUSD
    token0Price
    token1Price
  }
}
"""

MARKET_BY_ID_QUERY = """
query ($id:ID!) {
  market(id:$id){
    id
    token0 { symbol id }
    token1 { symbol id }
    reserveUSD
    token0Price
    token1Price
  }
}
"""

async def fetch_pendle_markets(chain="arbitrum", first=50, skip=0):
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(SUBGRAPH_URL,json={"query":MARKETS_QUERY,"variables":{"first":first,"skip":skip}})
        r.raise_for_status()
        data = r.json()
        return data.get("data",{}).get("markets",[])

async def fetch_market_by_id(chain="arbitrum", market_id=""):
    if not market_id: return None
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(SUBGRAPH_URL,json={"query":MARKET_BY_ID_QUERY,"variables":{"id":market_id}})
        r.raise_for_status()
        data = r.json()
        return data.get("data",{}).get("market")

