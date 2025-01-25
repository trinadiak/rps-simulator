# RPS Simulator
by Trinadia Kurniasari<br>
Department of Nuclear Engineering and Engineering Physics<br>
Universitas Gadjah Mada

Modification from the previous work:
[Suryono, T. J., Trianti, N., Santoso, S., Sudarno, Kiswanta, Maerani, R., & Kusriyanto, M. (2024). Data visualization in the human-machine interface of reactor protection system simulator. Jurnal Teknologi Reaktor Nuklir, 26(3), p. 107–114.](https://inis.iaea.org/records/2jm9c-5hb05)

## Abstract:<br>
The Reactor Protection System (RPS) plays a vital role in ensuring the safe operation of nuclear power plants by monitoring key reactor parameters and triggering automated shutdowns when necessary. The human-machine interface (HMI) of the RPS is crucial for allowing operators to effectively oversee, interpret, and respond to complex data. This study focuses on simulating the data flow within the RPS of HTR-10, a high-temperature gas-cooled reactor (HTGR) with a thermal power output of 10 MWth. The simulation aims to improve understanding of RPS functionality and enhance operators' awareness of plant parameter statuses. Using Python, HMI panels and sensor input data were developed to display critical sensor readings (neutron flux, helium temperature, and primary coolant pressure) and their trip setpoints through both static panels and real-time graphs. The HMI also indicates reactor status (normal or trip) based on the presence of trip signals in the RPS and generates alarm panels during reactor trips. This RPS simulator provides a valuable tool for guiding future advancements in reactor safety systems.

## Improved features:
1. Dynamic graphical visualization through bar charts
2. Switchable input control: automatic/manual
3. Data logging to csv file
4. Display of the historical sensor data
