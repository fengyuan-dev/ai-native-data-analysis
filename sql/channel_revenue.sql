SELECT
    u.acquisition_channel,
    SUM(o.amount) AS revenue
FROM orders AS o
JOIN users AS u
    ON o.user_id = u.user_id
WHERE o.status = 'paid'
  AND o.order_date >= DATE '2026-04-01'
  AND o.order_date < DATE '2026-05-01'
GROUP BY u.acquisition_channel
ORDER BY revenue DESC;