# MongoDB

## Commands

- Connect: `mongosh`
- Dump: `mongodump --db database`
- Restore: `mongorestore --db database`
- Export: `mongoexport --collection coll --out file.json`

## Best Practices

- Design documents based on access patterns, not normalization
- Use embedded documents for related data (avoid joins)
- Use indexes for fields used in queries and sorts
- Use `explain()` to analyze query performance
- Use MongoDB aggregation pipeline for complex queries
- Set appropriate TTL indexes for expiring data
- Use `ObjectId` for default `_id` or use UUIDs
- Use write concern `majority` for critical data
- Use replica sets for high availability
