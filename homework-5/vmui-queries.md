## 1. Внешняя доступность (TBSLI)

```promql
100 * avg_over_time(dormitory_helper_probe_success[5m])
```

Цель SLO отдельной серией:

```promql
99
```

## 2. Доступность HTTP-запросов (RBSLI)

```promql
100 * sum(rate(http_requests_total{status!~"5..",handler!="none"}[5m])) / sum(rate(http_requests_total{handler!="none"}[5m]))
```

Цель SLO:

```promql
99
```

## 3. Быстрые HTTP-запросы (RBSLI latency)

```promql
100 * sum(rate(http_request_duration_seconds_bucket{le="0.5",handler!="none"}[5m])) / sum(rate(http_request_duration_seconds_count{handler!="none"}[5m]))
```

Цель SLO:

```promql
95
```

## 4. Успешные входы (дополнительный бизнес-SLI)

```promql
100 * sum(dormitory_helper_user_logins_total{outcome="success"}) / sum(dormitory_helper_user_logins_total)
```

Цель SLO:

```promql
95
```

## 5. SLA и допустимый error budget

Фактическая доступность за 30 дней:

```promql
100 * avg_over_time(dormitory_helper_probe_success[30d])
```

Линия SLA:

```promql
98.5
```

Оставшийся месячный error budget в процентах от разрешённого простоя:

```promql
100 * (avg_over_time(dormitory_helper_probe_success[30d]) - 0.985) / (1 - 0.985)
```
