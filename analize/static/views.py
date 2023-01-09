from audioop import reverse
from cgi import test
from queue import Empty
from tempfile import tempdir
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import tabula
import pandas as pd
import numpy as np
import os
from .models import Mydata,Reference,Login,students_info
from django.db.models import F, Value
from django.db.models.functions import Concat


# Create your views here.

sem=0
rows=0
pass_y=0
pass_out_year=''
midroll=0
excel_sec_data={}
detain=[]
subjects=[]
abs_roll=[]
check=False
check_res=False
check_analyse=False
check_result_sub=False
context1={}
context2={} 
all_pass_bar=[]
all_fail_bar=[]
login_=True
dff=pd.DataFrame()
@csrf_exempt
def login(request):
    if request.method =="POST":
        uname=request.POST.get('uname')
        pwd=request.POST.get('pwd')

        data=Login.objects.filter(Username=uname,Password=pwd).count() 
        if(data>0):
            request.session.set_test_cookie()
            return render(request,'home.html')
    # return render(request,'home.html')
    return render(request,'login.html') 
def logout(request):
    request.session.delete_test_cookie()

    return redirect('login')
@csrf_exempt
def index(request):
    if request.session.test_cookie_worked():
    # Mydata.objects.all().delete()
    # Reference.objects.all().delete()
        
        return render(request,'home.html')  
    return render(request,'login.html')   
def batch(request):
    if request.session.test_cookie_worked():
        return render(request,'addbatch.html')  
    else:
        return redirect('login')
def home(request):
    if request.session.test_cookie_worked():

        global check
        
        # Mydata.objects.all().delete()
        # Reference.objects.all().delete()
        if(check==True):
            return render(request,'index.html',{'context':context1})    
        else: 
            return render(request,'home.html')
    else:
        return render(request,'login.html')   


@csrf_exempt
def func(request): 
    if request.session.test_cookie_worked():
        if request.method == 'POST':
            data=Mydata()
            reference=Reference()
            table2 = request.FILES['myFile']
            name__=str(table2)
            
            name_=name__.split('.')[0]
            df=tabula.read_pdf(table2,pages='all')
            df=pd.concat(df)
            df=df.drop([df.index[1], df.index[0]])
            # tabula.convert_into(table2, "media/"+name_+".csv", output_format="csv", pages='all')
            # file='media/'+name_+'.csv'
            # df = pd.read_csv('media/'+name_+'.csv')
            # df.to_csv('out2.csv')
            # if(os.path.exists(file) and os.path.isfile(file)):
            #         os.remove(file)
            df=df.dropna(subset=['Unnamed: 0'])
            global subjects
            subjects=list(df.columns)
            subjects.insert(0,"RollNo")
            subjects[1]="SGPA"
            subjects[2]="CGPA"
            subjects.pop()
            df.columns=subjects
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            global rows
            rows = df.shape[0]
            subjects=list(df.columns)
            subjects.remove('CGPA')
            subjects.remove('SGPA')
            subjects.remove('RollNo')
            df['Semester']=name_
            abs_lis = list(df.apply(lambda  x:",".join(x[x=='Ab'].index.values), axis = 1))
            df['Absenties']=abs_lis
            # abs_no=list(df['Absenties'].apply(lambda x : x if len(list(x.split(','))) ==len(subjects) else len(list(x.split(',')))))
            # abs_no = [int(i) for i in abs_no] 
            df['No_of_ab']='Nan'
            # temp_df=df[df['No_of_ab'] >=6]
            global abs_roll
            # abs_roll=list(temp_df["RollNo"])
            df = df[df['RollNo'].isin(abs_roll) == False] 
            df = df.reset_index()
            list4=[]
            abs_lis=df['Absenties']
            abs_no=df['No_of_ab']
            df=df.drop(columns=['Absenties','No_of_ab'])
            df['Failed_Subjects']="NaN"
            df['Passed_Subjects']="NaN"
            df['No_of_backlogs']='Nan'
            # df['Failed_Subjects']=df.apply(lambda rows :list4.append(x) for x in rows, axis = 1)
            failed=[]
            
            failed=list(df.apply(lambda  x:",".join(x[x=='F'].index.values), axis = 1))
        
            df['Failed_Subjects']=failed
            df2=df.drop(columns=['index','RollNo','SGPA','CGPA','Failed_Subjects','Passed_Subjects','Semester','No_of_backlogs'])
    
            df['Passed_Subjects']=list(df2.apply(lambda  x:",".join(x[(x!='F') & (x!='Ab')].index.values), axis = 1)) 
            # df['Passed Subjects']=list(df2.apply(lambda x:",".join(x[(x!='Ab') | (x!='F')].index.values),axis=1))
            df = df.reset_index()
            # df.apply(lambda rows : df['No_of_backlogs'][row]=0 if failed[row]=='' )
            for i in range(0,len(failed)):
                if(failed[i]==''):
                    df['No_of_backlogs'][i]=0
                else:
                    df['No_of_backlogs'][i]=len(list(failed[i].split(','))) 
            del df2
            df=df.drop(columns=['index'])
            
            for i in subjects:
                    df.drop(columns=i, axis=1, inplace=True)
            mid_roll=int(rows/2)
            midroll=df['RollNo'][mid_roll]
            passing_year=int(midroll[:2])+4
            df['Passed_Out_Year']=passing_year
            global pass_y
            pass_y=passing_year
            global sem
            sem=name_
            global detain
            detain=[]
            l=midroll[:2]
            global dff
            dff=df
            war_msg=None
            if  Reference.objects.filter(Passed_Out_Year='20'+str(pass_y), Semester=sem).exists():
                war_msg=(name__," Already exists")
            else: 
                war_msg=(" "+name__+" Uploded")
    

            subs={}
            for i in subjects:
                subs[i]=i
            df['Absent_subjects']=abs_lis
            df.to_csv('final.csv')
            global check_analyse
            check_analyse=True
            context={
                'war_msg':war_msg,
                'subjects':subjects,
            }
            return JsonResponse({'context':context})  
        return render(request,'index.html')
    return redirect('login')
def bar_graph(seca):
    all_pass=0
    all_fail=0
    Section_Pass_=[]
    Section_Fail_=[]
    for i in seca:
        fai=list(seca[i]['Failed_Subjects'])
        pass_=fai.count('')
        fail_=len(fai)-int(pass_)
        all_pass=all_pass+int(pass_)
        all_fail=all_fail+int(fail_)
        Section_Pass_.append(pass_) 
        Section_Fail_.append(fail_)
    return(all_pass,all_fail,Section_Pass_,Section_Fail_)


def area_graph(sem_graph,i):
    a_fai=list(sem_graph.loc[sem_graph['Semester'] == i, 'Failed_Subjects'])
    a_pass=a_fai.count('')
    a_fail=len(a_fai)-int(a_pass)
    return a_pass,a_fail
@csrf_exempt
def analyize(request):
    if request.session.test_cookie_worked():
        if request.method == 'POST':
            # if(check_analyse==True):
            y=str(pass_y-4)
            # df = pd.DataFrame(list(Mydata.objects.filter(Passed_Out_Year=pass_y,Semester=sem).values()))
            df=dff
            reference=Reference()
            global pass_out_year
            Final_df=df

            # checking if the result exists in database if not then it will upload
            if  Reference.objects.filter(Passed_Out_Year='20'+str(pass_y), Semester=sem).exists():
                pass
            else:
                df_temp = pd.DataFrame(list(students_info.objects.values()))
                Final_df=dff.merge(df_temp,on=['RollNo'])
                Final_df=Final_df.drop(columns=['level_0','No_of_backlogs_y','Semester_y','Passed_Subjects_y','Failed_Subjects_y','CGPA_y','SGPA_y','Passed_Out_Year_x'])
                Final_df.rename(columns = {'SGPA_x':'SGPA','CGPA_x':'CGPA','Semester_x':'Semester','Failed_Subjects_x':'Failed_Subjects','Passed_Subjects_x':'Passed_Subjects','Passed_Out_Year_y':'Passed_Out_Year','No_of_backlogs_x':'No_of_backlogs'}, inplace = True)
                Final_df['SGPA'] = Final_df['SGPA'].fillna('-')
                Final_df['CGPA'] = Final_df['CGPA'].fillna('-')
                Final_df['Failed_Subjects'] = Final_df['Failed_Subjects'].fillna('-')
                Final_df['Passed_Subjects'] = Final_df['Passed_Subjects'].fillna('-')
                Final_df.apply(lambda row :students_info.objects.filter(RollNo=row['RollNo']).update(SGPA=Concat(F('SGPA'),Value(row['SGPA']),Value('$')),CGPA=Concat(F('CGPA'),Value(row['CGPA']),Value('$')),Semester=Concat(F('Semester'),Value(row['Semester']),Value('$')),Failed_Subjects=Concat(F('Failed_Subjects'),Value(row['Failed_Subjects']),Value('$')),Passed_Subjects=Concat(F('Passed_Subjects'),Value(row['Passed_Subjects']),Value('$')),No_of_backlogs=Concat(F('No_of_backlogs'),Value(row['No_of_backlogs']),Value('$'))),axis=1)
                reference.Passed_Out_Year='20'+str(pass_y)
                reference.Semester=sem
                reference.Subjects=",".join(subjects)
                reference.Absenties=",".join(abs_roll)
                reference.save()
            # Final_df.apply(lambda row :students_info.objects.filter(RollNo=row['RollNo']).update(SGPA=Concat(F('SGPA'),Value(row['SGPA']),Value('$')),CGPA=Concat(F('CGPA'),Value(row['CGPA']),Value('$')),Semester=Concat(Value(F('Semester'),row['Semester']),Value('$')),Failed_Subjects=Concat(F('Failed_Subjects'),Value(row['Failed_Subjects']),Value('$')),Passed_Subjects=Concat(F('Passed_Subjects'),Value(row['Passed_Subjects']),Value('$'))),axis=1)
            ttemp=list(sem.split('-'))
            data_=pd.DataFrame(list(students_info.objects.filter(Passed_Out_Year='20'+str(pass_y),Semester__contains=sem).values()))

            data__=pd.DataFrame(list(students_info.objects.filter(Passed_Out_Year='20'+str(pass_y),Semester__contains=ttemp[2]).values()))

            data_['SGPA']=data_.apply(lambda row:row['SGPA'].split('$')[(row['Semester'].split('$')).index(sem)],axis=1)
            data_['CGPA']=data_.apply(lambda row:row['CGPA'].split('$')[(row['Semester'].split('$')).index(sem)],axis=1)
            data_['Passed_Subjects']=data_.apply(lambda row:row['Passed_Subjects'].split('$')[(row['Semester'].split('$')).index(sem)],axis=1)
            data_['Failed_Subjects']=data_.apply(lambda row:row['Failed_Subjects'].split('$')[(row['Semester'].split('$')).index(sem)],axis=1)
            data_['No_of_backlogs']=data_.apply(lambda row:int(row['No_of_backlogs'].split('$')[(row['Semester'].split('$')).index(sem)]),axis=1)
            data_['Semester']=sem

            allsems_pass_dict=[]
            allsems_fail_dict=[]
            allsems_sem_dict=[]


            all_sems=data__.Semester.unique()
            all_sems__ = list((max(all_sems, key = len)[:-1]).split('$'))
            all_sems__=set(all_sems__)
            for i in sorted(all_sems__):
                _data__=data__.loc[data__['Semester'].str.contains(i, case=False)]
                _data__['SGPA']=_data__.apply(lambda row:row['SGPA'].split('$')[(row['Semester'].split('$')).index(i)],axis=1)
                _data__['CGPA']=_data__.apply(lambda row:row['CGPA'].split('$')[(row['Semester'].split('$')).index(i)],axis=1)
                _data__['Passed_Subjects']=_data__.apply(lambda row:row['Passed_Subjects'].split('$')[(row['Semester'].split('$')).index(i)],axis=1)
                _data__['Failed_Subjects']=_data__.apply(lambda row:row['Failed_Subjects'].split('$')[(row['Semester'].split('$')).index(i)],axis=1)
                _data__['No_of_backlogs']=_data__.apply(lambda row:int(row['No_of_backlogs'].split('$')[(row['Semester'].split('$')).index(i)]),axis=1)
                _data__['Semester']=i
                fai=list(_data__['Failed_Subjects'])
                pass_=fai.count('')
                fail_=len(fai)-int(pass_)
                allsems_pass_dict.append(pass_)
                allsems_fail_dict.append(fail_)
                allsems_sem_dict.append(i)
            dict_temp={}
            sections=sorted(data_.Section.unique())
            data_=data_.sort_values('Section')
            for i in sections:
                mask_var = data_['Section'] ==i
                df1 = data_[mask_var]
                df1=df1.sort_values('RollNo')
                dict_temp[i]=df1
            #     df1, df2 = [x for _, x in data_.groupby(data_['Section'] ==i)]
            #     break
            df['Section']='Nan'
            sec_a_faculty=[]
            sec_b_faculty=[]
            sec_c_faculty=[]
            sec_d_faculty=[]
            sec_a_faculty=request.POST.getlist('a_')
            sec_b_faculty=request.POST.getlist('b_')
            sec_c_faculty=request.POST.getlist('c_')
            sec_d_faculty=request.POST.getlist('d_')
            faculty=[]
            if sec_a_faculty[0] !="NA":
                faculty=sec_a_faculty
            if sec_b_faculty[0] !="NA":
                faculty=faculty+sec_b_faculty
            if sec_c_faculty[0] !="NA":
                faculty=faculty+sec_b_faculty
            if sec_d_faculty[0] !="NA":
                faculty=faculty+sec_b_faculty
            all_pass,all_fail,Section_Pass ,Section_Fail=bar_graph(dict_temp)
            n=all_pass+all_fail
            per=(all_pass/n)*100
            Total_pass_percentage=round(per,2)
            pass_percentage=[]
            fail_percentage=[]
            for i in range(0,len(Section_Pass)):
                n=Section_Pass[i]+Section_Fail[i]
                per=(Section_Pass[i]/n)*100
                pass__=per
                pass_percentage.append(round(per,2))
                fail_percentage.append(round(100-float(pass__),2))
            # Total_analysis_pass=[Section_Pass,all_pass,n,Total_pass_percentage]
            Total_analysis_pass={}
            k=0
            for i in dict_temp:

                Total_analysis_pass[i]=Section_Pass[k]
                k=k+1
            Total_analysis_pass["All Sections Total"]=all_pass
            Total_analysis_pass["Total Students Appeared For exams"]=data_.shape[0]
            Total_analysis_pass["Pass Percentage"]=Total_pass_percentage
            

            
            sections_list=[]
            for i in dict_temp:
                sections_list.append(i)
            per_f=0
            per_p=0
            Total_subjects={}
            total_res=[]
            total=(','.join(data_['Failed_Subjects'].tolist())).split(',') 
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
                Total_subjects[i]=total_res
                total_res=[]
            temp_res={}
            Section_wise_result={}
            count=0
            for i in dict_temp:
                list4=(','.join(dict_temp[i]['Passed_Subjects'].tolist())).split(',') 
                k=0
                temp__res=[]
                for j in subjects:
                    a_rows = dict_temp[i].shape[0]
                    c=list4.count(j)
                    per_p=round((c/a_rows)*100,2)
                    if count>=len(faculty):
                        temp__res.append("-")
                    else:
                        temp__res.append(faculty[count])
                        
                    count+=1
                    temp__res.append(a_rows)
                    temp__res.append(c)
                    temp__res.append(a_rows-c)
                    temp__res.append(per_p)
                    temp_res[j]=temp__res
                    temp__res=[]
                Section_wise_result[i]=temp_res
                temp_res={}
            total_failed_ = Final_df['No_of_backlogs'][Final_df['No_of_backlogs'] >2 ].count()
            t_1_fail=(Final_df['No_of_backlogs'] == 1).sum()
            t_2_fail=(Final_df['No_of_backlogs'] == 2).sum()
            total_fail=[t_1_fail,t_2_fail,total_failed_]
            Total_analysis_fail={}
            for i in dict_temp:
                temp_failed_ = dict_temp[i]['No_of_backlogs'][dict_temp[i]['No_of_backlogs'] >2 ].count()
                temp_1_fail=(dict_temp[i]['No_of_backlogs'] == 1).sum()
                temp_2_fail=(dict_temp[i]['No_of_backlogs'] == 2).sum()
                temp_list=[temp_1_fail,temp_2_fail,temp_failed_]
                Total_analysis_fail[i]=temp_list
            Total_analysis_fail['Total']=total_fail
            # Toppers analysis
            total_top_table=Final_df.sort_values(by=['CGPA'], ascending=False)
            count_roll=0
            total_top_roll=[]
            total_top_cgpa=[] 
            total_top_table=total_top_table.reset_index()
            for i in range(total_top_table.shape[0]):
                if(total_top_table['CGPA'][i] not in "ABCDFA+B+C+-"):
                    q=total_top_table['RollNo'][i]
                    total_top_roll.append(q)
                    total_top_cgpa.append(total_top_table['CGPA'][i])
                    
                    count_roll+=1
                if count_roll==5:
                    break

            Section_wise_toppers={}
            for i in dict_temp:
                temp_top=dict_temp[i].sort_values(by=['CGPA'], ascending=False)
                temp_top_roll=[]
                temp_top_cgpa=[]
                count_roll=0
                temp_top=temp_top.reset_index()
                for j in range(temp_top.shape[0]):
                    if(temp_top['CGPA'][j] not in "ABCDFA+B+C+-"):
                        q=temp_top['RollNo'][j]
                        temp_top_roll.append(q)
                        temp_top_cgpa.append(temp_top['CGPA'][j])

                        count_roll+=1
                    if count_roll==5:
                        break

                Final_temp_sec={}
                for k in range(0,5):
                    Final_temp_sec[temp_top_roll[k]]=temp_top_cgpa[k]
                
                Section_wise_toppers[i]=Final_temp_sec
                Final_temp_sec={}
            total_top={}
            for i in range(0,5):
                total_top[total_top_roll[i]]=total_top_cgpa[i]
            df=df.drop(columns=['level_0','Absent_subjects','Section'])
            df=df.fillna('-')
            context={
                'n':all_pass+all_fail,
                'sem':sem,
                'lis':df,
                'all_pass':all_pass,
                'all_fail':all_fail,
                'Section_Pass':Section_Pass,
                'Section_Fail':Section_Fail,
                'pass_percentage':pass_percentage,
                'fail_percentage':fail_percentage,
                'sections_list':sections_list,
                'Total_top':total_top,
                'Section_wise_toppers':Section_wise_toppers,
                'Total_analysis_pass':Total_analysis_pass,
                'Total_analysis_fail':Total_analysis_fail,
                'Section_wise_result':Section_wise_result,
                'Total_subjects':Total_subjects,
                'allsems_pass_dict':allsems_pass_dict,
                'allsems_fail_dict':allsems_fail_dict,
                'allsems_sem_dict':allsems_sem_dict
            }
            return render(request,'index.html',{'context':context}) 


        return render(request,'index.html')
    else:
        return redirect('login')

@csrf_exempt
def retrive(request):
    if request.session.test_cookie_worked():
        ref=pd.DataFrame(list(Reference.objects.all().values()))    
        data_check=len(ref.index)
        if(data_check==0):
            return render(request,'home.html')
        else:
            sems__=ref['Semester']
            pass_year=(ref.Passed_Out_Year.unique()) 
            if request.method == 'POST':
                        _sem=request.POST.get('sem')
                        p_y=request.POST.get('passoutyear')
                        d=pd.DataFrame(Reference.objects.filter(Passed_Out_Year=p_y,Semester=_sem).values())
                        temp=d['Subjects'].tolist()
                        # subjects_=temp[2:-2]
                        subjects_=str(temp)
                        subjects__=str(subjects_[2:-2])
                        subjects=subjects__.split(',')
                        ttemp=list(_sem.split('-'))
                        data_=pd.DataFrame(list(students_info.objects.filter(Passed_Out_Year=p_y,Semester__contains=_sem).values()))

                        # data__=pd.DataFrame(list(students_info.objects.filter(Passed_Out_Year=p_y,Semester__contains=_sem).values()))
                        
                        data_['SGPA']=data_.apply(lambda row:row['SGPA'].split('$')[(row['Semester'].split('$')).index(_sem)],axis=1)
                        data_['CGPA']=data_.apply(lambda row:row['CGPA'].split('$')[(row['Semester'].split('$')).index(_sem)],axis=1)
                        data_['Passed_Subjects']=data_.apply(lambda row:row['Passed_Subjects'].split('$')[(row['Semester'].split('$')).index(_sem)],axis=1)
                        data_['Failed_Subjects']=data_.apply(lambda row:row['Failed_Subjects'].split('$')[(row['Semester'].split('$')).index(_sem)],axis=1)
                        data_['No_of_backlogs']=data_.apply(lambda row:int(row['No_of_backlogs'].split('$')[(row['Semester'].split('$')).index(_sem)]),axis=1)
                        data_['Semester']=sem
                        dict_temp={}
                        sections=sorted(data_.Section.unique())
                        data_=data_.sort_values('Section')
                        for i in sections:
                            mask_var = data_['Section'] ==i
                            df1 = data_[mask_var]
                            df1=df1.sort_values('RollNo')
                            dict_temp[i]=df1
                        all_pass,all_fail,Section_Pass ,Section_Fail=bar_graph(dict_temp)
                        n=all_pass+all_fail
                        per=(all_pass/n)*100
                        Total_pass_percentage=round(per,2)
                        pass_percentage=[]
                        fail_percentage=[]
                        for i in range(0,len(Section_Pass)):
                            n=Section_Pass[i]+Section_Fail[i]
                            per=(Section_Pass[i]/n)*100
                            pass__=per
                            pass_percentage.append(round(per,2))
                            fail_percentage.append(round(100-float(pass__),2))
                        # Total_analysis_pass=[Section_Pass,all_pass,n,Total_pass_percentage]
                        Total_analysis_pass={}
                        k=0
                        for i in dict_temp:

                            Total_analysis_pass[i]=Section_Pass[k]
                            k=k+1
                        Total_analysis_pass["All Sections Total"]=all_pass
                        Total_analysis_pass["Total Students Appeared For exams"]=data_.shape[0]
                        Total_analysis_pass["Pass Percentage"]=Total_pass_percentage
                        

                        
                        sections_list=[]
                        for i in dict_temp:
                            sections_list.append(i)
                        per_f=0
                        per_p=0
                        Total_subjects={}
                        total_res=[]
                        total=(','.join(data_['Failed_Subjects'].tolist())).split(',') 
                        for i in subjects:
                            _rows = data_.shape[0]
                            c=total.count(i)
                            per_f=round((c/_rows)*100,2)
                            per_p=round(100-per_f,2)
                            total_res.append(_rows)
                            total_res.append(_rows-c)
                            total_res.append(c)
                            total_res.append(per_p)
                            total_res.append(per_f)
                            Total_subjects[i]=total_res
                            total_res=[]
                        temp_res={}
                        Section_wise_result={}
                        for i in dict_temp:
                            list4=(','.join(dict_temp[i]['Passed_Subjects'].tolist())).split(',') 
                            k=0
                            temp__res=[]
                            for j in subjects:
                                a_rows = dict_temp[i].shape[0]
                                c=list4.count(j)
                                per_p=round((c/a_rows)*100,2)
                                temp__res.append('-')
                                temp__res.append(a_rows)
                                temp__res.append(c)
                                temp__res.append(a_rows-c)
                                temp__res.append(per_p)
                                temp_res[j]=temp__res
                                temp__res=[]
                            Section_wise_result[i]=temp_res
                            temp_res={}
                        total_failed_ = data_['No_of_backlogs'][data_['No_of_backlogs'] >2 ].count()
                        t_1_fail=(data_['No_of_backlogs'] == 1).sum()
                        t_2_fail=(data_['No_of_backlogs'] == 2).sum()
                        total_fail=[t_1_fail,t_2_fail,total_failed_]
                        Total_analysis_fail={}
                        for i in dict_temp:
                            temp_failed_ = dict_temp[i]['No_of_backlogs'][dict_temp[i]['No_of_backlogs'] >2 ].count()
                            temp_1_fail=(dict_temp[i]['No_of_backlogs'] == 1).sum()
                            temp_2_fail=(dict_temp[i]['No_of_backlogs'] == 2).sum()
                            temp_list=[temp_1_fail,temp_2_fail,temp_failed_]
                            Total_analysis_fail[i]=temp_list
                        Total_analysis_fail['Total']=total_fail
                        # Toppers analysis
                        total_top_table=data_.sort_values(by=['CGPA'], ascending=False)
                        count_roll=0
                        total_top_roll=[]
                        total_top_cgpa=[] 
                        total_top_table=total_top_table.reset_index()
                        for i in range(total_top_table.shape[0]):
                            if(total_top_table['CGPA'][i] not in "ABCDFA+B+C+-"):
                                x=total_top_table['Branch'][i]
                                y=total_top_table['Section'][i]
                                sec=x+" "+y
                                q=total_top_table['RollNo'][i]+"-"+sec
                                total_top_roll.append(q)
                                total_top_cgpa.append(total_top_table['CGPA'][i])
                                
                                count_roll+=1
                            if count_roll==5:
                                break

                        Section_wise_toppers={}
                        for i in dict_temp:

                            temp_top=dict_temp[i].sort_values(by=['CGPA'], ascending=False)
                            temp_top_roll=[]
                            temp_top_cgpa=[]
                            count_roll=0
                            temp_top=temp_top.reset_index()
                            for j in range(temp_top.shape[0]):
                                if(temp_top['CGPA'][j] not in "ABCDFA+B+C+-"):
                                    q=temp_top['RollNo'][j]
                                    temp_top_roll.append(q)
                                    temp_top_cgpa.append(temp_top['CGPA'][j])

                                    count_roll+=1
                                if count_roll==5:
                                    break

                            Final_temp_sec={}
                            for k in range(0,5):
                                Final_temp_sec[temp_top_roll[k]]=temp_top_cgpa[k]
                            
                            Section_wise_toppers[i]=Final_temp_sec
                            Final_temp_sec={}
                        

                        total_top={}
                        for i in range(0,5):
                            total_top[total_top_roll[i]]=total_top_cgpa[i]
                        ref=pd.DataFrame(list(Reference.objects.all().values()))    
                        sems__=ref['Semester']
                        pass_year=(ref.Passed_Out_Year.unique()) 

                        context={
                            'n':all_pass+all_fail,
                            'sem':_sem,
                            'all_pass':all_pass,
                            'all_fail':all_fail,
                            'Section_Pass':Section_Pass,
                            'Section_Fail':Section_Fail,
                            'pass_percentage':pass_percentage,
                            'fail_percentage':fail_percentage,
                            'sections_list':['A','B','C','D'],
                            'Total_top':total_top,
                            'pass_year':sorted(pass_year),
                            'Section_wise_toppers':Section_wise_toppers,
                            'Total_analysis_pass':Total_analysis_pass,
                            'Total_analysis_fail':Total_analysis_fail,
                            'Section_wise_result':Section_wise_result,
                            'Total_subjects':Total_subjects,
                        }
                        return render(request,'results.html',{'context':context})
                   
            ref=pd.DataFrame(list(Reference.objects.all().values()))    
            sems__=ref['Semester']
            pass_year=(ref.Passed_Out_Year.unique()) 
            if(check_res==False):
                context={
                    'sems__':sems__,
                    'pass_year':sorted(pass_year , reverse=True),
                }
                return render(request,'results.html',{'context':context})

            else:
                context2['sems__']=sems__
                context2['pass_year']=sorted(pass_year , reverse=True)
                return render(request,'results.html',{'context':context2})

    else:
        return redirect('login') 
@csrf_exempt        
def upload(request):
    if request.method == 'POST':
        reference=Reference()
        table2 = request.FILES['myFile']
        section_csv=pd.read_excel(table2)
        
        global pass_out_year
        pass_out_year=section_csv.columns[0]
        sections=[]
        dict1={}
        list1=[]
        d=section_csv.shape[0]
        for i in range(section_csv.shape[0]):
                if section_csv['Unnamed: 1'].isnull().iloc[i]:
                    list1.append(i)
                    sections.append(list(section_csv.iloc[i] )[0])
        k=0
        for i in list1:
            if(i== list1[-1]):
                dict1[sections[k]]=list(section_csv.loc[i+2:d-1, "Unnamed: 1"])
            else:
                dict1[sections[k]]=list(section_csv.loc[i+2:list1[k+1]-1, "Unnamed: 1"])
                k=k+1
        name__=str(table2)
            
        name_=name__.split('.')[0]
        global excel_sec_data
        new_data={}
        data=pd.DataFrame(students_info.objects.values())
        if(data.empty):
            excel_sec_data=dict1
        else:
            list2=list(data['RollNo'])
            year=''
            
            for i in dict1:
                year=dict1[i][0]
                break 
            for i in dict1:
                le=i.split('-')
                branch=le[0]
                section=le[1]
                list3=[]
                for j in dict1[i]:
                    c=list2.count(j)
                    if(c>0):
                        #exists in database
                        pass
                    else:
                        list3.append(j)
                        #does not exists in database

                new_data[i]=list3
            excel_sec_data=new_data
        
        return JsonResponse({'dict':excel_sec_data}) 
@csrf_exempt 
def sem(request):
    passyear=request.POST.get('passoutyear')
    data_2=pd.DataFrame(Reference.objects.filter(Passed_Out_Year=passyear).values("Semester"))
    
    sems_=list(data_2["Semester"]) 
    return JsonResponse({'sem':sems_})
@csrf_exempt      
def get(request):
    if request.session.test_cookie_worked():

        if request.method == 'POST':
            students=students_info()
            res=request.POST.getlist('checkbox')
            global excel_sec_data
            global pass_out_year
            for i in res:
                le=i.split('-')
                branch=le[0]
                section=le[1]
                for j in excel_sec_data[i]:
                    students.RollNo=j
                    students.Branch=branch
                    students.Section=section

                    students.Passed_Out_Year=pass_out_year
                    students.save()

            msg='successfully uploaded'
        return render(request,'addbatch.html',{'message':msg}) 