D=int(input('Uma Distancia em metros:'))
km= D/1000
hm= D/100
dam= D/10
dm= D*10
cm= D*100
mm= D*1000
print('A medida de {} corresponde a:'.format(D))
print('\n{}km \n{}hm \n{}dam \n{}dm \n{}cm \n{}mm'.format(km,hm,dam,dm,cm,mm))