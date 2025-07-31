import

{products}
from

'wix-stores.v2';

export async function
get_search(request)
{
    const
keyword = request.query.keyword?.toLowerCase();
const
limit = parseInt(request.query.limit) | | 200; // Default
limit

if (!keyword)
{
return {
    status: 400,
    body: {error: "Missing 'keyword' parameter"}
};
}

try {
// Initial server-side filtering
const {items} = await products.queryProducts()
.limit(limit)
.contains("name", keyword) // Basic server-side filtering
.find();

return {
    status: 200,
    body: {
        products: items,
        hasMore: items.length === limit // Indicates if more
results
exist
}
};
} catch(error)
{
return {
    status: 500,
    body: {error: "Search failed"}
};
}
}