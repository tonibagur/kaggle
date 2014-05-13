import psycopg2
import oct2py
import numpy

db=psycopg2.connect(user='coneptum',password='tumconep2012',database='allstate')
cur=db.cursor()

def create_join_table(table,length):
    #table='train'
    #length=12
    cur.execute('''
    select column_name from information_schema.columns where table_name='%s'
    order by ordinal_position'''%(table,))
    cols=[c[0] for c in cur.fetchall()]
    #print cols

    cols_new=[]
    for i in range(length):
        for c in cols:
            cols_new.append('t%d.%s %s_%d'%(i+1,c,c,i+1))
    for c in cols:
        cols_new.append('ty.%s %s_y'%(c,c,))

    from_clause=['%s t1' %(table,),'left outer join %s ty on(t1.customer_ID=ty.customer_ID and ty.record_type=1)'%(table,)]
    where_clause=['t1.shopping_pt=1','t1.record_type=0']
    for i in range(length-1):
        from_clause.append('left outer join %s t%d on (t1.customer_ID=t%d.customer_ID and t%d.record_type=0 and t%d.shopping_pt=%d)'%(table,i+2,i+2,i+2,i+2,i+2))

    #print cols_new
    #print from_clause

    stmt='''
    drop table if exists %s_join;
    create table %s_join as 
    select %s
    from %s
    where %s
    ''' % (table,table,','.join(cols_new),
           '\n'.join(from_clause),
           ' and '.join(where_clause),
          )
    print stmt
    cur.execute(stmt)
    db.commit()


num_bin_cols=['day','group_size','a','b','c','d','e','f','g']
char_bin_cols=['state','car_value','risk_factor','c_previous']
bin_cols=['homeowner','married_couple']
num_cols=['car_age','age_oldest','age_youngest']
print "Tenir en compte columna location si hi han problemes de BIAS!!!!"


def get_cols_vals(num_bin_cols,char_bin_cols,bin_cols,num_cols,table,length):
    print "Getting column values...."
    stmt2='''
    select trim(coalesce(to_char(%s_%s,'99999'),'UNKNOWN')),count(*)
    from %s_join
    group by trim(coalesce(to_char(%s_%s,'99999'),'UNKNOWN'))
    '''
    stmt3='''
    select trim(coalesce(%s_%s,'UNKNOWN')),count(*)
    from %s_join
    group by trim(coalesce(%s_%s,'UNKNOWN'))
    '''

    vals={}

    for c in num_bin_cols:
        stmts=[stmt2%(c,'y',table,c,'y')]
        vals[c]=set([])
        for i in range(length):
            s=stmt2%(c,str(i+1),table,c,str(i+1))
            stmts.append(s)
        for s in stmts:
            cur.execute(s)
            for x in cur.fetchall():
                vals[c]=vals[c]|set([x[0]])
    for c in char_bin_cols:
        stmts=[stmt3%(c,'y',table,c,'y')]
        vals[c]=set([])
        for i in range(length):
            s=stmt3%(c,str(i+1),table,c,str(i+1))
            stmts.append(s)
        for s in stmts:
            cur.execute(s)
            for x in cur.fetchall():
                vals[c]=vals[c]|set([x[0]])

    return vals

print '''TODO: Estudiar possibilitat de senyalitzar nuls a bin_cols i num_cols'''

def create_bin_table(table,column_sel,select,sufix,pk_create,num_bin_cols,char_bin_cols,bin_cols,num_cols,vals):
    print "creating table %s..."%(table,)
    for i in column_sel:
        for c in num_bin_cols:
            for v in sorted(list(vals[c])):
                select.append('''CASE WHEN trim(coalesce(to_char(%s_%s,'99999'),'UNKNOWN'))='%s' THEN 1 ELSE 0 END %s_%s_%s'''%(c,i,v,c,i,v))
        for c in char_bin_cols:
            for v in sorted(list(vals[c])):
                select.append('''CASE WHEN trim(coalesce(%s_%s,'UNKNOWN'))='%s' THEN 1 ELSE 0 END %s_%s_%s'''%(c,i,v,c,i,v))
        '''TODO: Estudiar possibilitat de senyalitzar nuls a bin_cols i num_cols'''
        for c in bin_cols + num_cols:
            select.append('''COALESCE(%s_%s,0) %s_%s'''%(c,i,c,i))

    stmt4='''
    drop table if exists %s_%s;
    create table %s_%s as
    select %s
    from %s_join''' %(table,sufix,table,sufix,',\n'.join(select),table)

    print stmt4
    cur.execute(stmt4)

    if pk_create:
        stmt5='alter table %s_%s add primary key(%s);'%(table,sufix,select[0])
        print stmt5
        cur.execute(stmt5)
    db.commit()


def get_np_array(from_table,order_criteria):
    cur.execute('''select * from {0} {1}'''.format(from_table,order_criteria))
    rows=cur.fetchall()
    return numpy.array(rows,dtype=float)
    

table='train'
length=12
'''create_join_table(table,length)'''
vals=get_cols_vals(num_bin_cols,char_bin_cols,bin_cols,num_cols,table,length)
'''
select=['customer_id_1']
selecty_a=['customer_id_1']
selecty_b=['customer_id_1']
selecty_c=['customer_id_1']
selecty_d=['customer_id_1']
selecty_e=['customer_id_1']
selecty_f=['customer_id_1']
selecty_g=['customer_id_1']

create_bin_table(table,map(lambda x:str(x+1),range(length)),select,'bin',True,num_bin_cols,char_bin_cols,bin_cols,num_cols,vals)
create_bin_table(table,['y'],selecty_a,'bin_y_a',True,['a'],[],[],[],vals)
create_bin_table(table,['y'],selecty_b,'bin_y_b',True,['b'],[],[],[],vals)
create_bin_table(table,['y'],selecty_c,'bin_y_c',True,['c'],[],[],[],vals)
create_bin_table(table,['y'],selecty_d,'bin_y_d',True,['d'],[],[],[],vals)
create_bin_table(table,['y'],selecty_e,'bin_y_e',True,['e'],[],[],[],vals)
create_bin_table(table,['y'],selecty_f,'bin_y_f',True,['f'],[],[],[],vals)
create_bin_table(table,['y'],selecty_g,'bin_y_g',True,['g'],[],[],[],vals)'''

'''
octave=oct2py.Oct2Py()
octave.put('X',get_np_array('train_bin','order by customer_id_1 asc'))
octave.put('y_a',get_np_array('train_bin_y_a','order by customer_id_1 asc'))
octave.put('y_b',get_np_array('train_bin_y_b','order by customer_id_1 asc'))
octave.put('y_c',get_np_array('train_bin_y_c','order by customer_id_1 asc'))
octave.put('y_d',get_np_array('train_bin_y_d','order by customer_id_1 asc'))
octave.put('y_e',get_np_array('train_bin_y_e','order by customer_id_1 asc'))
octave.put('y_f',get_np_array('train_bin_y_f','order by customer_id_1 asc'))
octave.put('y_g',get_np_array('train_bin_y_g','order by customer_id_1 asc'))
print octave.run('whos')
octave.run('save allstate.mat X y_a y_b y_c y_d y_e y_f y_g')'''

'''select_test=['customer_id_1']
create_join_table('test',length)
create_bin_table('test',map(lambda x:str(x+1),range(length)),select_test,'bin',True,num_bin_cols,char_bin_cols,bin_cols,num_cols,vals)
octave=oct2py.Oct2Py()
octave.put('X',get_np_array('test_bin','order by customer_id_1 asc'))
octave.run('save test_allstate.mat X')'''

def check_predictions(table,order,vals):
    errors_a=0
    errors_b=0
    errors_c=0
    errors_d=0
    errors_e=0
    errors_f=0
    errors_g=0
    errors=0
    octave=oct2py.Oct2Py()
    octave.load('y_predict_a.mat')
    a=octave.get('y')
    octave.load('y_predict_b.mat')
    b=octave.get('y')
    octave.load('y_predict_c.mat')
    c=octave.get('y')
    octave.load('y_predict_d.mat')
    d=octave.get('y')
    octave.load('y_predict_e.mat')
    e=octave.get('y')
    octave.load('y_predict_f.mat')
    f=octave.get('y')
    octave.load('y_predict_g.mat')
    g=octave.get('y')
    cur.execute('''select a_y,b_y,c_y,d_y,e_y,f_y,g_y from {0} {1}'''.format(table,order)) 
    rows=cur.fetchall()
    total=len(rows)
    for i,r in enumerate(rows):
        error=False
        if int(r[0])!=int(sorted(list(vals['a']))[int(a[i][0]-1)]):
            print "a", int(r[0]),sorted(list(vals['a']))[int(a[i][0]-1)]
            errors_a+=1
            error=True
        if int(r[1])!=int(sorted(list(vals['b']))[int(b[i][0]-1)]):
            errors_b+=1
            error=True
        if int(r[2])!=int(sorted(list(vals['c']))[int(c[i][0]-1)]):
            errors_c+=1
            error=True
        if int(r[3])!=int(sorted(list(vals['d']))[int(d[i][0]-1)]):
            errors_d+=1
            error=True
        if int(r[4])!=int(sorted(list(vals['e']))[int(e[i][0]-1)]):
            errors_e+=1
            error=True
        if int(r[5])!=int(sorted(list(vals['f']))[int(f[i][0]-1)]):
            errors_f+=1
            error=True
        if int(r[6])!=int(sorted(list(vals['g']))[int(g[i][0]-1)]):
            errors_g+=1
            error=True
        if error:
            errors+=1
    print "Errors a:",errors_a,float(errors_a)/float(total)
    print "Errors b:",errors_b,float(errors_b)/float(total)
    print "Errors c:",errors_c,float(errors_c)/float(total)
    print "Errors d:",errors_d,float(errors_d)/float(total)
    print "Errors e:",errors_e,float(errors_e)/float(total)
    print "Errors f:",errors_f,float(errors_f)/float(total)
    print "Errors g:",errors_g,float(errors_g)/float(total)
    print "Errors totals:",errors,float(errors)/float(total)
    

#check_predictions('train_join','order by customer_id_1 asc',vals)

def get_predictions(table,order,vals):
    fout=open('submit.csv','w')
    octave=oct2py.Oct2Py()
    octave.load('y_testpred_a.mat')
    a=octave.get('y')
    octave.load('y_testpred_b.mat')
    b=octave.get('y')
    octave.load('y_testpred_c.mat')
    c=octave.get('y')
    octave.load('y_testpred_d.mat')
    d=octave.get('y')
    octave.load('y_testpred_e.mat')
    e=octave.get('y')
    octave.load('y_testpred_f.mat')
    f=octave.get('y')
    octave.load('y_testpred_g.mat')
    g=octave.get('y') 
    fout.write("customer_ID,plan\n")  
    cur.execute('select customer_id_1 from {0} {1}'.format(table,order))
    for i,r in enumerate(cur.fetchall()):
        fout.write("{0},{1}{2}{3}{4}{5}{6}{7}\n".format( r[0],
                                                   int(sorted(list(vals['a']))[int(a[i][0]-1)]),
                                                   int(sorted(list(vals['b']))[int(b[i][0]-1)]), 
                                                   int(sorted(list(vals['c']))[int(c[i][0]-1)]),
                                                   int(sorted(list(vals['d']))[int(d[i][0]-1)]),
                                                   int(sorted(list(vals['e']))[int(e[i][0]-1)]),
                                                   int(sorted(list(vals['f']))[int(f[i][0]-1)]),
                                                   int(sorted(list(vals['g']))[int(g[i][0]-1)]) )    )
    fout.close()

get_predictions('test_join','order by customer_id_1 asc',vals)    


