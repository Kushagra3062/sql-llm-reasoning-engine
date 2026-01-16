// Simulate the AI processing delay
export const simulateProcessing = (ms = 1500) => new Promise(resolve => setTimeout(resolve, ms));

export const processQuery = async (query) => {
    await simulateProcessing();
    const q = query.toLowerCase();

    // SCENARIO 1: Simple - "How many customers are from Brazil?"
    if (q.includes('brazil') && q.includes('customer')) {
        return {
            role: 'system',
            content: "There are 5 customers from Brazil.",
            reasoning: [
                "Identified entity 'Customer'",
                "Checking schema for 'Customer' table. Found column 'Country'",
                "Formulating query to filter by Country = 'Brazil' and count"
            ],
            sql: "SELECT count(*) FROM Customer WHERE Country = 'Brazil';",
            data: {
                columns: ["Count"],
                rows: [["5"]]
            }
        };
    }

    // SCENARIO 2: Moderate - "Which 5 artists have the most tracks?"
    if ((q.includes('artist') && q.includes('most tracks')) || (q.includes('top') && q.includes('artist'))) {
        return {
            role: 'system',
            content: "Here are the top 5 artists with the most tracks:",
            reasoning: [
                "Identified entities 'Artist' and 'Track'",
                "Found relationship: Artist -> Album -> Track",
                "Strategy: JOIN Artist, Album, Track",
                "Group by ArtistId and Count TrackId",
                "Order by Count DESC, Limit 5"
            ],
            sql: `SELECT ar.Name, COUNT(t.TrackId) as TrackCount
FROM Artist ar
JOIN Album al ON ar.ArtistId = al.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
GROUP BY ar.Name
ORDER BY TrackCount DESC
LIMIT 5;`,
            data: {
                columns: ["Name", "TrackCount"],
                rows: [
                    ["Iron Maiden", "213"],
                    ["U2", "135"],
                    ["Led Zeppelin", "114"],
                    ["Metallica", "112"],
                    ["Deep Purple", "92"]
                ]
            }
        };
    }

    // SCENARIO 3: Reasoning - "Which customers have never made a purchase?"
    if (q.includes('never') && (q.includes('purchase') || q.includes('buy'))) {
        return {
            role: 'system',
            content: "All customers in the database have made at least one purchase. There are no customers without an invoice.",
            reasoning: [
                "Need customers with no invoices",
                "Checking schema... found Customer table, Invoice table",
                "Invoice has CustomerId as foreign key",
                "Strategy: LEFT JOIN, filter where InvoiceId is NULL"
            ],
            sql: `SELECT c.FirstName, c.LastName, c.Email
FROM Customer c
LEFT JOIN Invoice i ON c.CustomerId = i.CustomerId
WHERE i.InvoiceId IS NULL;`,
            data: {
                columns: ["FirstName", "LastName", "Email"],
                rows: [] // Empty result
            }
        };
    }

    // SCENARIO 4: Ambiguous - "Show me recent orders"
    if (q.includes('recent') && q.includes('order')) {
        return {
            role: 'system',
            content: "I can show you recent orders, but 'recent' is ambiguous. Do you mean from the last 30 days, or the last year of data (2013)?",
            // No SQL or Data yet, just clarifying
        };
    }

    // SCENARIO 4b: Follow up "Last year" or "2013"
    if (q.includes('2013') || q.includes('last year')) {
        return {
            role: 'system',
            content: "Here are the total sales for the year 2013.",
            reasoning: [
                "Filter InvoiceDate for year 2013",
                "Sum Total column"
            ],
            sql: `SELECT SUM(Total) as TotalSales FROM Invoice WHERE strftime('%Y', InvoiceDate) = '2013';`,
            data: {
                columns: ["TotalSales"],
                rows: [["450.58"]]
            }
        };
    }

    // Default / Fallback
    return {
        role: 'system',
        content: "I understand the concept, but I don't have the specific logic for that query in my demo mode yet. Try asking: 'Which 5 artists have the most tracks?' or 'How many customers are from Brazil?'"
    };
};
