[Aaron Townsend](/users/atownsend)
Effective Date
June 15, 2009
Abstract
A method for quantitatively comparing dissimilar ventilation systems has been developed. A calibrated ventilation model was exercised over a range of parameters seen in new and existing housing in the United States. Varied parameters included climate, building enclosure air leakage, presence or absence of a central forced-air space conditioning system, ventilation system type, ventilation airflow rate, and contaminant generation locations.
Text
### **Introduction**
ASHRAE Standard 62.2–2007 — Ventilation and Acceptable Indoor Air Quality in Low-Rise Residential Buildings (ASHRAE 2008) (furthermore referred to in this paper simply as "Standard 62.2") sets minimum required ventilation rates for residential dwelling units. The amount of air prescribed by the standard is determined by the size of the dwelling and the number of occupants, typically determined from the number of bedrooms. No further instruction is given as to what type of ventilation system is acceptable. This omission may lead some users of the standard to believe that all ventilation systems that provide the same amount of air provide the same benefit. This is in fact not the case.
Past work has shown that different residential ventilation systems do not provide equivalent performance even when providing the same nominal outside air flow rate. For example, Hendron (2007) found that when interior doors were closed, an exhaust-only ventilation system provides less uniform distribution of ventilation air than a ventilation system that incorporates the central air handler to periodically mix the spaces. Sherman (2008) found that exposure levels calculated from tracer gas testing within a house depended strongly on the ventilation system and assumptions about the pollutant source and occupant location.
The purpose of the work described in this paper is to address this particular weakness in Standard 62.2. It is an attempt to quantitatively compare many existing ventilation systems and provide a method for adjusting the Standard 62.2 ventilation rate for a house based on the type of ventilation system installed. This method results in a coefficient assigned to each ventilation system (CS) that modifies the current Standard 62.2 mechanical ventilation rate. This would result in an equation of the form shown in Equation 1:
*Q fan* = *C S* • *Q vent* (1)
Where
 *Q fan* = required ventilation system flow rate  
 *C S* = system coefficient (assigned based on the ventilation system selected)  
*Q vent* = the minimum mechanical ventilation flow rate required by Standard 62.2.
Townsend (2009) demonstrated that it was possible to replicate field measurements in a calibrated computer model to predict the performance of different ventilation systems under similar conditions; however this work was limited to a  
single, two-story house in one climate and was not directly applicable to the entire stock of existing and new residential homes in the United States. The range of climates and house characteristics, especially the building enclosure air leakage rate, across the U.S. heavily influence the performance of ventilation systems.
The work described in this paper addresses some of the limitations of the work in Townsend (2009) by exercising a similar computer model over a wide range of climates and building enclosure air leakage rates. By doing so, this work covers a much larger subset of typical single-family houses found in the United States. Next, by choosing a reference ventilation system for baseline performance, the ventilation systems considered in this work are evaluated in the manner described above and their equivalency determined. The end goal is to show how this method works and assign example system coefficient to each of the several ventilation systems considered.
### **Description of Computer Model**
This work follows previous work (Townsend 2009) in which CONTAM, a multi-zone airflow modeling program (Walton 2005, Dols 2001) was used in a calibrated model of one house to reproduce the results of field tests and then to predict the performance of ventilation systems that were not tested in the field. In the current work, the CONTAM model was used in a similar fashion, except that instead of duplicating the results from one specific house, it was exercised over a range of parameters in order to cover a reasonable subset of the new and existing houses in the United States. This range of parameters and the input assumptions used came about through consensus agreement working directly with ASHRAE Standing Standards Project Committee 62.2 members over the course of several meetings from 2006 to 2009.
#### House Characteristics
A single house plan was used in this study. The house modeled is a two-story, approximately 2600 sf (240 m2) house with four bedrooms and three bathrooms. The first floor consists of one bedroom, one bathroom, a laundry/utility room, a living room, and a kitchen/dining room. The second floor consists of the master bedroom and master bathroom, two additional bedrooms, one additional bathroom, and a small area at the top of the stairway overlooking living room below. In the model, each room with a closeable door was modeled as a separate zone with the exception of closets, which were modeled as part of the room they were connected to. The kitchen was modeled as a separate zone from the living room even though there was no closeable door between the two. The arrangement of the zones in the house is shown in Figure 1 and the relevant zone attributes are listed in Table 1. The house has a garage and vented attic that were both neglected in the computer model; these spaces were modeled as outdoors.
**![](https://www.buildingscience.com/sites/default/files/cp-0908_figure_01.jpg?itok=92j8oRJl)**
**Figure 1:** Zones in the modeled house.
**Table 1:** Zone Attributes
![](https://www.buildingscience.com/sites/default/files/cp-0908_table_01.jpg?itok=Mw3F2EpH)
#### Occupancy
Two occupants were assigned to the master bedroom and a single occupant was assigned to each of the remaining bedrooms, for a total of five occupants in the four-bedroom house. Each occupant was assumed to follow the same schedule each day, as described in Table 2. As the occupants moved around the house on their daily schedule, they were exposed to the pollutants in that location.
**Table 2:** Occupancy Schedules
![](https://www.buildingscience.com/sites/default/files/cp-0908_table_02.jpg?itok=KqVTdIyw)
#### ASHRAE Standard 62.2 Mechanical Ventilation Rate
The ASHRAE 62.2 minimum required mechanical ventilation rate for this house and occupancy is 63 cfm (30 L/s).
#### Bedroom Doors
All doorways were modeled with appropriate sized openings that allowed two-way flow due to temperature differences between the rooms. Bedroom doors were assumed to be open except during the sleeping period of 10:00 PM to 7:00 AM.
#### Interior Temperature
Each zone temperature was held constant at either 71.6 or 71.63 °F (22 or 22.015 °C). The small temperature difference was used to cause thermally-driven two-way flow through open doorways as occurs naturally in buildings. In reality temperature differences between zones are likely to be larger than these; however when larger temperature differences were used in the model unrealistically high two-way flows resulted through the doorways (about 225 cfm (113 L/s) with a 2 °F (1 °C) temperature difference). As modeled the temperature difference resulted in flow of about 30 cfm (15 L/s) in each direction through the bedroom doorways and about 140 cfm (70 L/s) through the opening between the kitchen and the living area. Small changes in interior temperatures will make little difference in the natural infiltration rate except during very mild outdoor conditions.
#### Contaminant Generation
Unique contaminants were generated in each zone of the house and by each of the occupants. The contaminants are generic (i.e. they are not a specific chemical) and are assumed to be non-reacting. This simplifying assumption results in the ability to consider different contaminant-generation scenarios in post-processing, while only running one CONTAM simulation per combination of inputs. Reacting contaminants and removal mechanisms other than dilution by outside air are beyond the scope of this work. It is also important to note that the generation rate is arbitrary; therefore it is the relative values of the contaminant concentrations with respect to other ventilation systems that are meaningful, rather than the absolute values.
#### Enclosure Leakage
Enclosure leakage was varied from very tight to very leaky. Total enclosure leakage was divided between walls, ceilings, and ducts. The first floor was assumed to be a slab-on-grade with no air leakage. The proportion of enclosure leakage assigned to each enclosure component (walls, ceiling, or ducts) changed during the different rounds of analysis, but was always based on Dickerhoff (1982) and Harrje (1982) as summarized in ASHRAE (2005) and was modified based on the engineering judgment of the research team. The specific proportion assigned to each of the enclosure components is listed in the description of each round of analysis later in this report. Enclosure leakage pathways were assumed to follow the power law model as described in Equation 2:
*Q = C • (∆P) n * (2)
Where
Q = volumetric leakage rate through leakage pathway  
C = leakage coefficient  
ΔP = pressure difference across leakage pathway  
n = leakage exponent = 0.65 (ASHRAE 2005, page 27.12)
#### Enclosure Leakage Locations
While the total enclosure leakage was varied (and is described later), the locations of the leakage pathways were held constant. The house was assumed to have a slab-on-grade foundation, so there were no leakage paths through the first floor. Diffuse leakage over the entire wall area was approximated by assigning five discrete leakage pathways along each vertical section of the wall, at 2.25 ft (0.686 m) intervals starting at 0 ft (0 m) above the surface of the first floor and extending all the way up to the surface of the ceiling on the second floor. Uniform ceiling leakage was approximated by assigning a single discrete leakage pathway for each ceiling, as there is no spatial dependency in the horizontal plane within each zone. Each wall or ceiling leakage pathway was assigned leakage characteristics as follows:
*C i/Ct* = *A i/At* (3)
Where
 *C i* = total leakage coefficient for wall or ceiling i  
 *C t* = total leakage coefficient for all walls or ceilings in the house  
 *A i* = exterior area of wall or ceiling i  
 *A t* = total exterior area of all walls or ceilings in the house
#### Climate
Various climates were simulated. Cities were chosen as representative of their respective climates (based on the Department of Energy/2006 IECC climate zone map (Briggs 2003)), and TMY2 weather data (Marion 1995) from that city was used for the outdoor temperature, wind speed, and wind direction. The cities considered in each round of analysis are discussed later.
#### Wind Pressure
Leakage due to wind pressure was modeled for all of the wall leakage pathways. The wind speed and direction was obtained from TMY2 data (Marion 1995) for each site. The surroundings were assumed to be suburban and a wind pressure modifier was used to account for the difference in wind speed between the weather measurement site and the site of the modeled house. The components of the wind speed pressure modifier were *Ao* = 0.6 and a = 0.28, as described in Walton (2005) and ASHRAE (1993). Average wind pressure coefficients were assumed to be 0.6 with the wind blowing directly towards the wall, -0.3 with the wind blowing directly away from the wall, and -0.65 with the wind blowing parallel to the wall. Intermediate angles were interpolated based on the equation developed by Walker (1994) as described in ASHRAE (2005). Wind was neglected for the ceiling leakage pathways due to the large dependence on the shape and pitch of the roof assembly, and the authors’ success in replicating experimental data in previous work while similarly neglecting wind effects on ceiling leakage (Townsend 2009).
**Table 3:** Air Conditioner Sizes and AHU Flow Rates
![](https://www.buildingscience.com/sites/default/files/cp-0908_table_03.jpg?itok=-uJAnhWU)
#### Air Handler Size and Operation
The air handler unit (AHU) size for each climate was determined by the cooling requirement for that climate as determined using a common commercial software that performs ACCA Manual J (ACCA 2003) calculations. Table 3 contains the results of these calculations. The heating airflow was assumed to be 85% of the cooling airflow. An AHU was not present in all of the cases simulated; if it was present, its operation each hour of the year was scheduled based on the TMY2 data for each climate and the following assumptions:
  1. At the climate’s heating or cooling design temperature, the AHU runs 80% of the time.
  2. Between the heating and cooling balance points, the AHU does not run for space conditioning, but may run according to a minimum runtime or minimum turnover criteria.
  3. Between the balance and design points, the AHU runs as described in Equation 4 below: . .


Download complete document [here](/file/3744).