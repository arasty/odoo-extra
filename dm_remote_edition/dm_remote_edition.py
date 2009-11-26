# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields
from osv import osv
import pooler
import re
import base64
pattern = re.compile("/Count\s+(\d+)")
class dm_mail_service(osv.osv): # {{{
    _inherit = "dm.mail_service"
    
    _columns = {
          'default_printer': fields.char('Default Printer', size=64),
          'default_printer_tray': fields.char('Default Printer Tray', size=64),
          'user_id': fields.many2one('res.users', 'Printer User'),
          'sorting_rule_id': fields.many2one('dm.campaign.document.job.sorting_rule', 'Sorting Rule'),
          'front_job_recap': fields.many2one('dm.offer.document', 'Front Job Recap'),
          'bottom_job_recap': fields.many2one('dm.offer.document', 'Bottom Job Recap'),

        }
dm_mail_service() # }}}


class dm_campaign_document_job(osv.osv): # {{{
    _inherit = "dm.campaign.document.job"
    
    _columns = {
         'user_id': fields.many2one('res.users', 'Printer User'),
         'use_front_recap': fields.boolean('Use Front Job Recap'),
         'use_bottom_recap': fields.boolean('Use Bottom Job Recap'),
        }
  
dm_campaign_document_job() # }}}

def generate_document_job(cr, uid, obj_id):
    pool = pooler.get_pool(cr.dbname)
    camp_doc_object = pool.get('dm.campaign.document')
    obj = camp_doc_object.browse(cr,uid,[obj_id])[0]
    ms_id = obj.mail_service_id
    type_id = pool.get('dm.campaign.document.type').search(cr, uid, [('code', '=', 'pdf')])[0]
    sql = 'select id from dm_campaign_document where mail_service_id = %d and type_id=%d and campaign_document_job is null'%(ms_id.id,type_id)
    cr.execute(sql)
    camp_doc_id = map(lambda x: x[0] ,cr.fetchall())
    s_rule = ms_id.sorting_rule_id.by_customer_country
    camp_doc_job = {}
    if ms_id.sorting_rule_id.by_customer_country:
	    for camp_doc in camp_doc_object.browse(cr,uid,camp_doc_id):
		    country_id = str(camp_doc.address_id.country_id.id)
		    if country_id in camp_doc_job:
			    camp_doc_job[country_id].append(camp_doc.id)
		    else : 
			    camp_doc_job[country_id] = [camp_doc.id]
    if ms_id.sorting_rule_id.by_offer_step:
        if not camp_doc_job:
            camp_doc_job['']=camp_doc_id
        camp_doc_job_i = {}
        for k,v in camp_doc_job.items() :
            for camp_doc in camp_doc_object.browse(cr,uid,v):
	            step_id = k+'_'+str(camp_doc.document_id.step_id.id)
	            if step_id in camp_doc_job_i:
		            camp_doc_job_i[step_id].append(camp_doc.id)
	            else : 
		            camp_doc_job_i[step_id] = [camp_doc.id]
        camp_doc_job = camp_doc_job_i
#    elif ms_id.sorting_rule_id.by_product:
#	    for camp_doc in camp_doc_object.browse(cr,uid,camp_doc_id):
#		    step_id = camp_doc.document_id.step_id.id
#		    if step_id in camp_doc_job:
#			    camp_doc_job[step_id].append(camp_doc.id)
#		    else : 
#			    camp_doc_job[step_id] = [camp_doc.id]
    if ms_id.sorting_rule_id.by_page_qty:
        if not camp_doc_job:
            camp_doc_job['']=camp_doc_id
        camp_doc_job_i = {}
        attach_obj = pool.get('ir.attachment')
        pattern = re.compile(r"/Count\s+(\d+)")
        for k,v in camp_doc_job.items() :
            for camp_doc in camp_doc_object.browse(cr,uid,v):
                attach_id = attach_obj.search(cr, uid,[('res_id', '=', camp_doc.id), 
        	                           ('res_model', '=', 'dm.campaign.document')])
                if attach_id:
                    attach = attach_obj.browse(cr, uid, attach_id[0])
                    datas = base64.decodestring(attach.datas)
                    vPages = k+'_'+str(pattern.findall(datas) and pattern.findall(datas)[0] or 0)
                else:
                    vPages = k
                if vPages in camp_doc_job_i :
    			    camp_doc_job_i[vPages].append(camp_doc.id)
                else : 
    			    camp_doc_job_i[vPages] = [camp_doc.id]
                    			    
        camp_doc_job = camp_doc_job_i        			    
    if camp_doc_job:
        camp_doc_job_obj = pool.get('dm.campaign.document.job')
        job_ids = camp_doc_job_obj.search(cr, uid, [('state', '=', 'pending'),
                            ('sorting_rule_id', '=', ms_id.sorting_rule_id.id),])

        job_id = {}
        for j_id in camp_doc_job_obj.browse(cr, uid, job_ids):
            if not ms_id.sorting_rule_id.qty_limit or ms_id.sorting_rule_id.qty_limit ==0 :
                job_id[j_id.sorting_name] = [j_id.id, len(j_id.campaign_document_ids), 0]
            elif len(j_id.campaign_document_ids) < ms_id.sorting_rule_id.qty_limit:
                job_id[j_id.sorting_name] = [j_id.id, len(j_id.campaign_document_ids), ms_id.sorting_rule_id.qty_limit]
        for k,v in camp_doc_job.items():
            while v:
                doc_job_camp_id = v.pop()
                if k in job_id.keys() and (job_id[k][-1] == 0 or job_id[k][1] < job_id[k][-1]) :
                    camp_doc_job_obj.write(cr, uid, job_id[k][0], 
                                       {'campaign_document_ids': [[4,doc_job_camp_id]]})
                    job_id[k][1] += 1
                else:
                    doc_count=1
                    camp_doc = camp_doc_object.browse(cr,uid,doc_job_camp_id)
                    vals = {
                            'name': camp_doc.segment_id.name or '' + str(k),
				         	'user_id': ms_id.user_id.id,
					        'sorting_rule_id': ms_id.sorting_rule_id.id,
					        'campaign_document_ids': [[4,doc_job_camp_id]],
                            'sorting_name': k,
                            'use_front_recap': ms_id.front_job_recap and True or False,
                            'bottom_job_recap': ms_id.bottom_job_recap and True or False,
                            }
                    j_id = camp_doc_job_obj.create(cr,uid,vals)
                    if  ms_id.front_job_recap or ms_id.bottom_job_recap:
                        doc_count = doc_count + 1
                        if ms_id.front_job_recap:
                            camp_vals={
                                   'segment_id': camp_doc.segment_id.id or False,
                                   'name': camp_doc.document_id.step_id.code + "_" + str(camp_doc.address_id.id),
                                   'type_id': type_id,
                                   'mail_service_id': ms_id.id,
                                   'document_id': ms_id.front_job_recap.id,
                                   'campaign_document_job_ids': j_id,
                                   'address_id':camp_doc.address_id.id 
                              }
                            camp_document = camp_doc_object.create(cr, uid, camp_vals)
                        if ms_id.bottom_job_recap:
                            doc_count = doc_count + 1
                            camp_vals={
                                   'segment_id': camp_doc.segment_id.id or False,
                                   'name': camp_doc.document_id.step_id.code + "_" + str(camp_doc.address_id.id),
                                   'type_id': type_id,
                                   'mail_service_id': ms_id.id,
                                   'document_id': ms_id.bottom_job_recap.id,
                                   'campaign_document_job_ids': j_id,
                                   'address_id':camp_doc.address_id.id 
                                  }
                            camp_document = camp_doc_object.create(cr, uid, camp_vals)
                    job_id[k] = [j_id, doc_count, ms_id.sorting_rule_id.qty_limit or 0]
    return {'code':'doc_done','ids': obj.id}								   		    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
