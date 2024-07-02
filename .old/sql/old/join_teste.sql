SELECT fluxo.name, module.name, service.name, process.name, subprocess.name, credencial.login, credencial.password, site.url
FROM fluxo_web
JOIN fluxo ON fluxo_web.id_fluxo = fluxo.id
JOIN module ON fluxo.id_module = module.id
JOIN service ON fluxo.id_service = service.id
JOIN process ON fluxo.id_process = process.id
JOIN subprocess ON fluxo.id_subprocess = subprocess.id
JOIN credencial ON fluxo_web.id_credencial = credencial.id
JOIN site ON fluxo_web.id_site = site.id;

SELECT 
fluxo_web.id AS fluxo_web_id,
fluxo.name AS fluxo_name, 
module.name AS module_name, 
service.name AS service_name,
process.name AS process_name, 
subprocess.name AS subprocess_name, 
credencial.login AS credencial_login, 
credencial.password AS credencial_password, 
site.url AS site_url
FROM fluxo_web
LEFT JOIN fluxo ON fluxo_web.id_fluxo = fluxo.id
LEFT JOIN module ON fluxo.id_module = module.id
LEFT JOIN service ON fluxo.id_service = service.id
LEFT JOIN process ON fluxo.id_process = process.id
LEFT JOIN subprocess ON fluxo.id_subprocess = subprocess.id
LEFT JOIN credencial ON fluxo_web.id_credencial = credencial.id
LEFT JOIN site ON fluxo_web.id_site = site.id;