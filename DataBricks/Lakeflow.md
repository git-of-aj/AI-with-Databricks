## [Ms Docs](https://learn.microsoft.com/en-us/azure/databricks/data-engineering/)
```txt
ADF / Fabric
     │
     ├── Copy Activity
     ├── Data Flow
     ├── Notebook
     ├── SQL activity
     └── Pipeline orchestration
             │
             ↓
       ADLS / Warehouse / Lakehouse
```
With Lakeflow:
```txt
             Lakeflow
                │
        ┌───────┴────────┐
        │                │
   Transformations    Orchestration
     SQL/Python       Dependencies
        │                │
        └───────┬────────┘
                ↓
          Delta tables
                ↓
         Unity Catalog

```

| Traditional ADF / Synapse / Fabric pipeline | Lakeflow                                 |
|---------------------------------------------|-----------------------------------------|
| Pipeline-centric                            | Data-centric                            |
| You define activities and their sequence   | You define datasets and transformations |
| Orchestration is explicit                   | Dependency orchestration is automatic   |
| Incremental logic often needs to be designed| Incremental processing is fundamental   |
| CDC/SCD often requires custom MERGE framework | AUTO CDC handles much of it declaratively |
| Data quality often implemented as activities/frameworks | Expectations are part of dataset definitions |
| Orchestrates multiple services/engines     | Deeply integrated with Spark + Delta + Unity Catalog |

> ADF/Fabric traditionally tells compute services when and how to execute ETL; Lakeflow lets you declare what the data should become and moves much of the incremental processing, dependency management, CDC, quality enforcement and execution management into the data pipeline engine itself.
