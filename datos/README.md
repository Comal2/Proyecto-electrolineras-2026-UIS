### ¿Para qué sirve `estadisticas.xlsx`? 
Actualmente **no se usa**, y está vacío de forma intencional. 
Este archivo está reservado para la **fase P2** del proyecto, donde se ejecutará la simulación del comportamiento de los vehículos eléctricos. Durante dicha simulación: 
* Cada vez que un vehículo realice una recarga, el sistema escribirá **una fila** en este archivo. 
*  Cada fila representará un evento de carga con información como, por ejemplo: 
	* Vehículo 
	* Electrolinera utilizada 
	* Nivel de batería al llegar
	* Hora simulada de la recarga 
==(COLUMAS MERAMENTE REPRESENTATIVAS, POR DEFINIR)==

Al finalizar todas las simulaciones, este archivo contendrá **cientos de registros**, los cuales serán utilizados en la **fase P3** para entrenar un modelo de *Machine Learning* que permitirá **predecir ubicaciones óptimas para nuevas electrolineras**. Por el momento, el archivo debe mantenerse vacío y la función asociada en el código puede permanecer comentada hasta que inicie P2.
