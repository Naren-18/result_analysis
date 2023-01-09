
                total_pass_per=round((sum(all_pass_bar)/result.shape[0])*100,2)
                pass_percentage=[]
                fail_percentage=[]
                for i in range(0,len(all_pass_bar)):

                    n=all_pass_bar[i]+all_fail_bar[i]
                    per=(all_pass_bar[i]/n)*100
                    pass_percentage.append(round(per,2))
                
                per_f=0
                per_p=0
                dict_s={}
                total_res=[]
                total=(','.join(df['Failed_Subjects'].tolist())).split(',') 
                for i in subjects:
                    _rows = df.shape[0]
                    c=total.count(i)
                    per_f=round((c/_rows)*100,2)
                    per_p=round(100-per_f,2)
                    total_res.append(_rows)
                    total_res.append(_rows-c)
                    total_res.append(c)
                    total_res.append(per_p)
                    total_res.append(per_f)
                    dict_s[i]=total_res
                    total_res=[]
                # toal subjects are calculate above 
                # now calculate the individual sections below
                seca_res={}
                secb_res={}
                secc_res={}
                secd_res={}
                sec_a_res=[]
                sec_b_res=[]
                sec_c_res=[]
                sec_d_res=[]
                #print("AAAAAAAAAAAAA")
                list1=(','.join(seca['Passed_Subjects'].tolist())).split(',') 
                list2=(','.join(secb['Passed_Subjects'].tolist())).split(',') 
                list3=(','.join(secc['Passed_Subjects'].tolist())).split(',') 
                list4=(','.join(secd['Passed_Subjects'].tolist())).split(',') 
                #print(list1)
                k=0
                for i in subjects:
                    a_rows = seca.shape[0]
                    c=list1.count(i)
                    per_p=round((c/a_rows)*100,2)
                    sec_a_res.append(sec_a_faculty[k])
                    sec_a_res.append(a_rows)
                    sec_a_res.append(c)
                    sec_a_res.append(a_rows-c)
                    sec_a_res.append(per_p)
                    seca_res[i]=sec_a_res
                    sec_a_res=[]
                    b_rows = secb.shape[0]

                    c=list2.count(i)
                    per_p=round((c/b_rows)*100,2)
                    sec_b_res.append(sec_b_faculty[k])

                    sec_b_res.append(b_rows)
                    sec_b_res.append(c)
                    sec_b_res.append(b_rows-c)
                    sec_b_res.append(per_p)

                    secb_res[i]=sec_b_res
                    sec_b_res=[]
                    c_rows = secc.shape[0]
                    c=list3.count(i)
                    per_p=round((c/c_rows)*100,2)
                    sec_c_res.append(sec_c_faculty[k])

                    sec_c_res.append(c_rows)
                    sec_c_res.append(c)
                    sec_c_res.append(c_rows-c)
                    sec_c_res.append(per_p)

                    secc_res[i]=sec_c_res
                    sec_c_res=[]
                    d_rows = secd.shape[0]
                    c=list4.count(i)
                    per_p=round((c/d_rows)*100,2)
                    sec_d_res.append(sec_d_faculty[k])

                    sec_d_res.append(d_rows)
                    sec_d_res.append(c)
                    sec_d_res.append(d_rows-c)
                    sec_d_res.append(per_p)
                    secd_res[i]=sec_d_res
                    sec_d_res=[]
                    k=k+1
                    
                # for i in range(0,len(subjects)):
                #     sec_a_res.insert(1,sec_a_faculty[i])
                #     sec_b_res.insert(1,sec_b_faculty[i])
                #     sec_c_res.insert(1,sec_c_faculty[i])
                #     sec_d_res.insert(1,sec_d_faculty[i])
                result = result.drop('level_0', 1)
                
                        # else:
                            # print("Detains and lES are not all selected")
                # Count number of True in series

                

                # Total_3_failed = len(total_failed_[total_failed_ == True].index)
                total_failed_ = result['No_of_backlogs'][result['No_of_backlogs'] >2 ].count()
                t_1_fail=(result['No_of_backlogs'] == 1).sum()
                t_2_fail=(result['No_of_backlogs'] == 2).sum()

                a_1_fail=(seca['No_of_backlogs'] == 1).sum()
                a_2_fail=(seca['No_of_backlogs'] == 2).sum()
                a_3_failed_ = seca['No_of_backlogs'][seca['No_of_backlogs'] >2 ].count()


                b_1_fail=(secb['No_of_backlogs'] == 1).sum()
                b_2_fail=(secb['No_of_backlogs'] == 2).sum()
                b_3_failed_ = secb['No_of_backlogs'][secb['No_of_backlogs'] >2 ].count()



                c_1_fail=(secc['No_of_backlogs'] == 1).sum()
                c_2_fail=(secc['No_of_backlogs'] == 2).sum()
                c_3_failed_ = secc['No_of_backlogs'][secc['No_of_backlogs'] >2 ].count()



                d_1_fail=(secd['No_of_backlogs'] == 1).sum()
                d_2_fail=(secd['No_of_backlogs'] == 2).sum()
                d_3_failed_ = secd['No_of_backlogs'][secd['No_of_backlogs'] >2 ].count()


                eee=a_3_failed_+b_3_failed_+c_3_failed_+d_3_failed_


                A_sec_failed=[a_1_fail,a_2_fail,a_3_failed_]
                B_sec_failed=[b_1_fail,b_2_fail,b_3_failed_]
                C_sec_failed=[c_1_fail,c_2_fail,c_3_failed_]
                D_sec_failed=[d_1_fail,d_2_fail,d_3_failed_]
                T_sec_failed=[t_1_fail,t_2_fail,total_failed_]
                sem_graph=pd.DataFrame(list(students_info.objects.filter(Passed_Out_Year='20'+str(pass_y)).values()))
                
                sems=list(set(sem_graph['Semester']))
                # sem_graph=[0,0,0,0]
                # sems=[0,0,0,0]
                sem_pass=[]
                sem_fail=[]
                for i in sorted(sems):
                    k,j=area_graph(sem_graph,i)
                    sem_pass.append(k)
                    sem_fail.append(j)
                # n=n_pass_bar+n_fail_bar
                n=2
                
                table=Mydata.objects.filter(Passed_Out_Year=pass_y,Semester=sem)
                # print(type(list(result['CGPA'])[0]))
        
                total_top_table=result.sort_values(by=['CGPA'], ascending=False)
                A_top_table=seca.sort_values(by=['CGPA'], ascending=False)
                B_top_table=secb.sort_values(by=['CGPA'], ascending=False)
                C_top_table=secc.sort_values(by=['CGPA'], ascending=False)
                D_top_table=secd.sort_values(by=['CGPA'], ascending=False)
                # total_top_table.drop(columns=['SGPA']) 
                var1=total_top_table[['RollNo','CGPA']].iloc[0:5]
                total_top_roll=list(var1['RollNo'])
                total_top_cgpa=list(var1['CGPA'])

                var1=A_top_table[['RollNo','CGPA']].iloc[0:5]
                A_top_roll=list(var1['RollNo'])
                A_top_cgpa=list(var1['CGPA'])

                var1=B_top_table[['RollNo','CGPA']].iloc[0:5]
                B_top_roll=list(var1['RollNo'])
                B_top_cgpa=list(var1['CGPA'])

                var1=C_top_table[['RollNo','CGPA']].iloc[0:5]
                C_top_roll=list(var1['RollNo'])
                C_top_cgpa=list(var1['CGPA'])

                var1=D_top_table[['RollNo','CGPA']].iloc[0:5]
                D_top_roll=list(var1['RollNo'])
                D_top_cgpa=list(var1['CGPA'])
                total_top={}
                a_top={}
                b_top={}
                c_top={}
                d_top={}

                for i in range(0,5):
                    total_top[total_top_roll[i]]=total_top_cgpa[i]
                    a_top[A_top_roll[i]]=A_top_cgpa[i]
                    b_top[B_top_roll[i]]=B_top_cgpa[i]
                    c_top[C_top_roll[i]]=C_top_cgpa[i]
                    d_top[D_top_roll[i]]=D_top_cgpa[i]
                # print(all_pass_bar)



                global context1 
                global check
                check=True
                context1={ 
                    'n':n,
                    # 'np':n_pass_bar,
                    # 'nf':n_fail_bar,
                    'sem':sem,
                    'lis':table,
                    'dict_s':dict_s, 
                    'seca_res':seca_res,
                    'secb_res':secb_res,
                    'secc_res':secc_res,
                    "secd_res":secd_res,
                    'A_sec_failed':A_sec_failed,
                    'B_sec_failed':B_sec_failed,
                    'C_sec_failed':C_sec_failed,
                    'D_sec_failed':D_sec_failed,
                    'T_sec_failed':T_sec_failed,
                    'pass_':all_pass_bar,
                    'fail_':all_fail_bar,
                    'sem_pass':sem_pass,
                    'aa':aa,
                    'bb':bb,
                    'cc':cc,
                    'dd':dd,
                    'sem_fail':sem_fail,
                    'sems':sorted(sems),
                    'total_pass_per':total_pass_per,
                    'pass_percentage':pass_percentage,
                    'fail_percentage':fail_percentage,
                    'total_top_roll':total_top_roll,
                    'total_top_cgpa':total_top_cgpa,
                    'A_top_roll':A_top_roll,
                    'A_top_cgpa':A_top_cgpa,
                    'B_top_roll':B_top_roll,
                    'B_top_cgpa':B_top_cgpa,
                    'C_top_roll':C_top_roll,
                    'C_top_cgpa':C_top_cgpa,
                    'D_top_roll':D_top_roll,
                    'D_top_cgpa':D_top_cgpa,

                    'total_top':total_top,
                        'a_top':a_top,
                        'b_top':b_top,
                        'c_top':c_top,
                        'd_top':d_top,

                }
                return render(request,'index.html',{'context':context1}) 
            else:
                errmsg="Upload a file to analyse"
                context={
                    'errmsg':errmsg,
                }
                return render(request,'home.html',{'context':context})
<tr class="bg-secondary text-white">
                                              <th colspan="6">D Section Toppers</th>
                                          </tr>
                                          
                                          <tr>
                                            <th scope="col" colspan='1'>Sno</th>
                                            <th scope="col" colspan='2' style="width:47%">RollNo</th>
                                            <th scope="col" colspan='3'>CGPA</th>
                                          </tr>
                                        </thead>
                                        <tbody>
                                          <!--Keep For loop for each Subject-->
                                          {%for i,j in context.d_top.items%}
                                          <tr>
                                            <td colspan='1'>*</td>
                                            <td colspan='2'>{{i}}</td>
                                            <td colspan='3'>{{j}}</td>
                                          </tr>
                                          {%endfor%}