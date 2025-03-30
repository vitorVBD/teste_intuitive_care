
WITH ultimo_trimestre AS (
    SELECT MAX(competencia) AS data_final 
    FROM demonstracoes_contabeis
)
SELECT 
    o.razao_social,
    o.nome_fantasia,
    o.uf,
    SUM(d.valor) AS total_despesas,
    COUNT(DISTINCT d.competencia) AS trimestres_considerados
FROM 
    demonstracoes_contabeis d
JOIN 
    operadoras o ON d.registro_ans = o.registro_ans
CROSS JOIN 
    ultimo_trimestre ut
WHERE 
    d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND d.competencia >= DATE_SUB(ut.data_final, INTERVAL 3 MONTH)
GROUP BY 
    o.razao_social, o.nome_fantasia, o.uf
ORDER BY 
    total_despesas DESC
LIMIT 10;

-- 2. Top 10 operadoras com maiores despesas no último ano
WITH ultimo_ano AS (
    SELECT MAX(competencia) AS data_final 
    FROM demonstracoes_contabeis
)
SELECT 
    o.razao_social,
    o.nome_fantasia,
    o.uf,
    SUM(d.valor) AS total_despesas,
    COUNT(DISTINCT d.competencia) AS trimestres_considerados
FROM 
    demonstracoes_contabeis d
JOIN 
    operadoras o ON d.registro_ans = o.registro_ans
CROSS JOIN 
    ultimo_ano ua
WHERE 
    d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND d.competencia >= DATE_SUB(ua.data_final, INTERVAL 1 YEAR)
GROUP BY 
    o.razao_social, o.nome_fantasia, o.uf
ORDER BY 
    total_despesas DESC
LIMIT 10;