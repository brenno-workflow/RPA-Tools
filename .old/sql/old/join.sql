SELECT 
    m.name AS module_name,
    s.name AS service_name,
    p.name AS process_name,
    sp.name AS subprocess_name,
    c.login AS credential_login,
    c.password AS credential_password,
    site.url AS site_url
FROM fluxo_web fw
JOIN fluxo f ON fw.id_fluxo = f.id
JOIN module m ON f.id_module = m.id
JOIN service s ON f.id_service = s.id
JOIN process p ON f.id_process = p.id
LEFT JOIN subprocess sp ON f.id_subprocess = sp.id
LEFT JOIN credencial c ON fw.id_credencial = c.id
JOIN site ON fw.id_site = site.id;

SELECT 
    m.name AS module_name,
    s.name AS service_name,
    p.name AS process_name,
    sp.name AS subprocess_name,
    c.login AS credential_login,
    c.password AS credential_password,
    site.url AS site_url
FROM fluxo_web fw
JOIN fluxo f ON fw.id_fluxo = f.id
JOIN module m ON f.id_module = m.id
JOIN service s ON f.id_service = s.id
JOIN process p ON f.id_process = p.id
JOIN subprocess sp ON f.id_subprocess = sp.id
JOIN credencial c ON fw.id_credencial = c.id
JOIN site ON fw.id_site = site.id;

SELECT 
    m.name AS module_name,
    s.name AS service_name,
    p.name AS process_name,
    sp.name AS subprocess_name,
    c.login AS credential_login,
    c.password AS credential_password,
    site.url AS site_url
FROM fluxo_web fw
JOIN module m ON fw.id_module = m.id
JOIN service s ON fw.id_service = s.id
JOIN process p ON fw.id_process = p.id
JOIN subprocess sp ON fw.id_subprocess = sp.id
JOIN credencial c ON fw.id_credencial = c.id
JOIN site ON fw.id_site = site.id;