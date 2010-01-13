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

import pooler
from report.interface import report_rml
from tools import to_xml

class survey_browse_response(report_rml):
    def create(self, cr, uid, ids, datas, context):

        rml ="""
                <document filename="Survey Analysis Report.pdf">
                <template pageSize="(595.0,842.0)" title="Test" author="Martin Simon" allowSplitting="20">
                    <pageTemplate id="first">
                      <frame id="first" x1="57.0" y1="57.0" width="481" height="728"/>
                </pageTemplate>
                  </template>
                  <stylesheet>
                    <blockTableStyle id="Table1">
                      <blockAlignment value="LEFT"/>
                      <blockValign value="TOP"/>
                      <lineStyle kind="LINEBELOW" colorName="#e6e6e6"/>
                    </blockTableStyle>
                    <blockTableStyle id="Table2">
                      <blockAlignment value="LEFT"/>
                      <blockValign value="TOP"/>
                    </blockTableStyle>
                    <blockTableStyle id="Table3">
                      <blockAlignment value="LEFT"/>
                      <lineStyle kind="LINEBELOW" colorName="#e6e6e6" start="1,0" stop="2,-1"/>
                      <blockValign value="TOP"/>
                    </blockTableStyle>
                    <blockTableStyle id="Table4">
                      <blockAlignment value="LEFT"/>
                      <blockValign value="TOP"/>
                      <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="1,-1"/>
                    </blockTableStyle>
                    <blockTableStyle id="Table5">
                      <blockAlignment value="LEFT"/>
                      <blockValign value="TOP"/>
                      <lineStyle kind="LINEBELOW" colorName="#8f8f8f" start="0,-1" stop="1,-1"/>
                    </blockTableStyle>
                    <initialize>
                      <paraStyle name="all" alignment="justify"/>
                    </initialize>
                    <paraStyle name="answer_right" alignment="RIGHT" fontName="helvetica" fontSize="09.0" leftIndent="2.0"/>
                    <paraStyle name="Standard1" fontName="helvetica-bold" alignment="RIGHT" fontSize="09.0"/>
                    <paraStyle name="Standard" alignment="LEFT" fontName="Helvetica-Bold" fontSize="11.0"/>
                    <paraStyle name="header1" fontName="Helvetica" fontSize="11.0"/>
                    <paraStyle name="response" fontName="Helvetica-oblique" fontSize="9.5"/>
                    <paraStyle name="page" fontName="helvetica" fontSize="11.0" leftIndent="0.0"/>
                    <paraStyle name="question" fontName="helvetica-boldoblique" fontSize="10.0" leftIndent="3.0"/>
                    <paraStyle name="answer_bold" fontName="Helvetica-Bold" fontSize="09.0" leftIndent="2.0"/>
                    <paraStyle name="answer" fontName="helvetica" fontSize="09.0" leftIndent="2.0"/>
                    <paraStyle name="answer1" fontName="helvetica" fontSize="09.0" leftIndent="2.0"/>
                    <paraStyle name="Title" fontName="helvetica" fontSize="20.0" leading="15" spaceBefore="6.0" spaceAfter="6.0" alignment="CENTER"/>
                    <paraStyle name="P2" fontName="Helvetica" fontSize="14.0" leading="15" spaceBefore="6.0" spaceAfter="6.0"/>
                    <paraStyle name="comment" fontName="Helvetica" fontSize="14.0" leading="50" spaceBefore="0.0" spaceAfter="0.0"/>
                    <paraStyle name="P1" fontName="Helvetica" fontSize="9.0" leading="12" spaceBefore="0.0" spaceAfter="1.0"/>

                  </stylesheet>
                  <images/>
                  <story>
                    <para style="Title"><u>Browse Responses </u></para>
                    <para style="Standard"><font></font></para>"""
        surv_resp_obj = pooler.get_pool(cr.dbname).get('survey.response')
        surv_resp_line_obj = pooler.get_pool(cr.dbname).get('survey.response.line')
        surv_obj = pooler.get_pool(cr.dbname).get('survey')
        for response in surv_resp_obj.browse(cr,uid, surv_resp_obj.search(cr,uid, [('survey_id','=',ids[0])])):
            for survey in surv_obj.browse(cr, uid, ids):
                rml += """
                        <blockTable colWidths="150,350" style="Table2">
                          <tr>
                            <td><para style="Standard">Survey Title :-</para></td>
                            <td><para style="header1">""" + to_xml(survey.title) + """</para></td>
                          </tr>
                          <tr>
                            <td><para style="Standard">Response Create Date :-</para></td>
                            <td><para style="header1">""" + to_xml(response.date_create) + """</para></td>
                            </tr>
                            <tr>
                            <td><para style="Standard">User Name :-</para></td>
                            <td><para style="header1">""" + to_xml(response.user_id.name) + """</para></td>
                          </tr>
                        </blockTable> """
                for page in survey.page_ids:
                    rml += """<para style="P2"></para>"""
                    rml += """ <blockTable colWidths="500" style="Table4">
                                  <tr>
                                    <td><para style="page">Page :- """ + to_xml(page.title) + """</para></td>
                                  </tr>
                               </blockTable>"""
                    for que in page.question_ids:
                        rml += """<para style="P2"></para>"""
                        rml +="""<blockTable colWidths="500" style="Table5">
                                  <tr>
                                    <td><para style="question">Que: """ + to_xml(que.question) + """</para></td>
                                  </tr>
                                 </blockTable>"""
                        answer = surv_resp_line_obj.browse(cr,uid, surv_resp_line_obj.search(cr, uid, [('question_id','=',que.id),('response_id','=',response.id)]))
                        if que.type in ['multiple_choice_only_one_ans','multiple_choice_multiple_ans']:
                            if len(answer) and answer[0].state == "done":
                                for ans in answer[0].response_answer_ids:
                                    rml +="""<blockTable colWidths="500" style="Table1">
                                         <tr> <td> <para style="response">""" + to_xml(ans.answer_id.answer) + """</para></td></tr>
                                        </blockTable>"""
                            else:
                                rml +="""<blockTable colWidths="500" style="Table1">
                                 <tr>  <td> <para style="response">No Response</para></td> </tr>
                                </blockTable>"""
                        elif que.type in ['multiple_textboxes','date','date_and_time','numerical_textboxes']:
                            if len(answer) and answer[0].state == "done":
                                for ans in answer[0].response_answer_ids:
                                    rml +="""<blockTable colWidths="200,300" style="Table1">
                                         <tr> <td> <para style="response">""" + to_xml(ans.answer_id.answer) + """</para></td>
                                         <td> <para style="response">""" + to_xml(ans.answer) + """</para></td></tr>
                                        </blockTable>"""
                            else:
                                rml +="""<blockTable colWidths="500" style="Table1">
                                 <tr>  <td> <para style="response">No Response</para></td> </tr>
                                </blockTable>"""
                        elif que.type in ['single_textbox']:
                            if len(answer) and answer[0].state == "done":
                                rml +="""<blockTable colWidths="500" style="Table1">
                                     <tr> <td> <para style="response">""" + to_xml(answer[0].single_text) + """</para></td></tr>
                                    </blockTable>"""
                            else:
                                rml +="""<blockTable colWidths="500" style="Table1">
                                 <tr>  <td> <para style="response">No Response</para></td> </tr>
                                </blockTable>"""
                        elif que.type in ['comment']:
                            if len(answer) and answer[0].state == "done":
                                rml +="""<blockTable colWidths="500" style="Table1">
                                     <tr> <td> <para style="response">""" + to_xml(answer[0].comment) + """</para></td></tr>
                                    </blockTable>"""
                            else:
                                rml +="""<blockTable colWidths="500" style="Table1">
                                 <tr>  <td> <para style="response">No Response</para></td> </tr>
                                </blockTable>"""
                        elif que.type in ['matrix_of_choices_only_one_ans','matrix_of_choices_only_multi_ans','rating_scale','matrix_of_drop_down_menus']:
                            if len(answer) and answer[0].state == "done":
                                cols_widhts = []
                                cols_widhts.append(200)
                                for col in range(0, len(que.column_heading_ids)):
                                    cols_widhts.append(float(300 / (len(que.column_heading_ids))))
                                colWidths = ",".join(map(str, cols_widhts))
                                matrix_ans = ['',]
                                for col in que.column_heading_ids:
                                    if col.title not in matrix_ans:
                                        matrix_ans.append(col.title)
                                rml+="""<blockTable colWidths=" """ + colWidths + """ " style="Table1"><tr>"""
                                for mat_col in matrix_ans:
                                    rml+="""<td><para style="response">""" + to_xml(mat_col) + """</para></td>"""
                                rml +="""</tr>"""
                                for ans in que.answer_choice_ids:
                                    rml+="""<tr><td><para style="response">""" + to_xml(ans.answer) + """</para></td>"""
                                    for mat_col in range(1, len(matrix_ans)):
                                        value = """"""
                                        for res_ans in answer[0].response_answer_ids:
                                            if res_ans.answer_id.id == ans.id and res_ans.answer == matrix_ans[mat_col]:
                                                if que.type in ['matrix_of_drop_down_menus']:
                                                    value = """<para style="response">""" + to_xml(str(res_ans.value_choice)) + """</para>"""
                                                elif que.type in ['matrix_of_choices_only_one_ans','rating_scale']:
                                                    value = """<illustration><fill color="gray"/>
                                                            <circle x="0.3cm" y="-0.18cm" radius="0.22 cm" fill="no" stroke="yes"/>
                                                            <circle x="0.3cm" y="-0.18cm" radius="0.10 cm" fill="yes" stroke="no"/>
                                                        </illustration>"""
                                                else:
                                                    value = """<illustration>
                                                        <rect x="0.1cm" y="-0.45cm" width="0.5 cm" height="0.5cm" fill="no" stroke="yes"/>
                                                        <fill color="gray"/>
                                                        <rect x="0.2cm" y="-0.35cm" width="0.3 cm" height="0.3cm" fill="yes" stroke="no"/>
                                                        </illustration>"""
                                        rml+= """<td>""" + value + """</td>"""
                                    rml+="""  </tr>"""
                                rml+="""</blockTable>"""
                            else:
                                rml +="""<blockTable colWidths="500" style="Table1">
                                 <tr>  <td> <para style="response">No Response</para></td> </tr>
                                </blockTable>"""
            rml += """<pageBreak/>"""
        rml += """</story></document>"""
        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)
        return (pdf, report_type)
    
survey_browse_response('report.survey.browse.response', 'survey','','')