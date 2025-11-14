## Technical Assessment: Commercial Real Estate Analytics API - Tech Lead
### Overview

The assessment is split into two sections:
1. API development
2. System design and planning

For the API development, please use either FastAPI OR Django rest framework.

I've provided two files: `market_data.json` and `property_data.json` which demonstrate the data structures you'll be working with.

You are welcome to use AI to help you write code, as long as it is used in a controlled manner and you can explain reasoning behind decisions. 

### Data Source Assumptions

For this assessment, please assume:
- **Market Data**: The `market_data.json` file shows the format of market data that will be retrieved from an external API (see [External Market Data API specification](EXTERNAL_MARKET_DATA_API.md))
- **Property Data**: The `property_data.json` represents data stored in and retrieved from a local database

### Business Context

As a CRE professional, you need to assess how your properties are performing relative to market averages across geographic regions. The API you develop will power dashboards that help investment teams make data-driven decisions about their real estate assets, including historical performance trends and comparative analysis.

### Timeframe Guidelines

We recommend ~2 hours spent on this task:
- **45 minutes** on API development
- **60 minutes** on architecture design, scalability planning, and system design documentation

## Section 1: Core API Development (45 minutes)

### Single Asset Performance API

`/api/properties/{propertyId}/market-performance`

Create an endpoint to compare an individual property (from `property_data.json`) against its latest local market benchmarks.

**Consider**:

- Metric filtering -> comparison to specific metrics
- Cache requirements/ performance and usage

**Bonus considerations**:
- Historic market analysis showing property performance trends relative to market trends over time


## Section 2: System design planning (60 minutes)

Design an extensible system for monitoring property performance relative to market data, including a **property health scoring mechanism**.

The goal of this work is to produce a design for a system which will drive a dashboard used by analytical users to flexibly interrogate and analyze performance of their assets.

### Goal: Design how we would implement a **property health scoring system**

This would be a way to compare assets to one another, suggest outliers or under-performers, and ways to generate insights.

We would like you to suggest the best way to produce this 'score' based on the provided information.

Considerations:
- External Market Data API integration
- Local database interactions optimized for health score queries
- Service architecture: health score calculation service, comparison engine, trend analyzer
- Request/response flow for property health score retrieval
- Error handling, fallback mechanisms, and circuit breakers
- Cache invalidation and data freshness management

Other general:
- Speed of data retrieval
- Calculation timing
- Scalability considerations for 1000+ properties across 50+ markets
- Time bucketing e.g. if users want to see monthly, quarterly, yearly bucketed data

*You do not need to cover all of these, but you should be able to talk about them in the follow-up conversation*

**Please produce:**
1. A diagram or visual aid to talk about system design/ architecture and tooling choices. 
2. A UML/ database schema diagram for your performance calculations and health scoring system.
3. Notes detailing your own considerations, drawbacks for decisions and future enhancement suggestions


### What We're Looking For

As a Tech Lead, we want to see:
- Understanding of implementation at both code and infrastructure levels
- Ability to make and justify architectural trade-offs
- Consideration of operational concerns (monitoring, debugging, maintenance)
- Clear communication of complex technical concepts
- Production-ready thinking (error handling, testing strategies, observability)
- Business value orientation (e.g., how property health scores drive investment decisions)
- Data quality awareness and handling of real-world data imperfections

