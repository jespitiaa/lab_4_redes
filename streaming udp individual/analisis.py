def main():
    enviados=13780*150
    recibidos=0
    perdidos=0
    tieSum=0
    tieTrans=0
    fc=open("UDPClientResults.txt", "r")
    fs=open("UDPServerResults.txt", "r")
    e=open("AnalisisUDP.txt","a+")
    lfc=fc.readlines()
    for x in lfc:
        arr=x.split("; ")
        rec=arr[0]
        tie=arr[1]
        rec=rec.replace("Se recibieron: ","")
        rec=rec.replace(" paquetes en el cliente","")
        recibidos=recibidos+int(rec)
        tie=tie.replace("Tiempo de atencion cliente: ", "")
        tieSum=tieSum+float(tie)
        print(recibidos)
        print(tie)
    lfs=fs.readlines()
    for y in lfs:
        arr=y.split(" Tiempo de transmision de ")
        print(arr)
        tieTrans=tieTrans+float(arr[1])
    perdidos=enviados-recibidos
    print(perdidos)
    e.write("Se perdieron "+str(perdidos)+" paquetes de un total de "+str(enviados)+" paquetes enviados; El tiempo promedio de atencion a un cliente es de "+str(tieSum/150)+" segundos; El throughput es de: "+str(enviados/tieTrans)+" paquetes/segundo\r\n")
if __name__ == '__main__':
    main()
