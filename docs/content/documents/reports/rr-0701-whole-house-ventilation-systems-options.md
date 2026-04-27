[Joseph Lstiburek](/users/jlstiburek), [Betsy Pettit](/users/bpettit), [Armin Rudd](/users/arudd)
Effective Date
April 05, 2007
Abstract
This paper reviews current ventilation codes and standards for residential buildings in Europe and North America. It also examines the literature related to these standards such as occupant surveys of attitudes and behavior related to ventilation, and research papers that form the technical basis of the ventilation requirements in the standards. The major findings from the literature are that ventilation is increasingly becoming recognized as an important component of a healthy dwelling, that the ventilation standards tend to cluster around common values for recommended ventilation rates, and that surveys of occupants showed that people generally think that ventilation is important, but that their understanding of the ventilation systems in their houses is low.
Text
### **1\. Summary of Technical Review of Literature (Task 1)**
A comprehensive literature review was made to investigate whole house ventilation system options, various simulation and engineering analysis tools and techniques, and baselines for comparing the current project results.
The literature reviewed included the following:
  * Literature listed in the request for proposal (RFP)
  * Literature referenced in the project proposal (See REFERENCES)
  * Literature listed in the residential ventilation list of the Lawrence Berkeley Laboratory (<http://epb.lbl.gov/Publications/ventilation.html>)


Additionally the proprietary database of the Air Infiltration and Ventilation Centre, AIRBASE, (<http://www.aivc.org>) was searched for relevant literature. AIRBASE contains over 15000 references related to air infiltration and ventilation and is the worlds' most authoritative source on the topic.
The deliverable for Task 1 is in the form of two LBNL reports -- one on Residential Ventilation Requirements, and one on Residential Ventilation Technologies, as follows:
McWilliams, J.A. and M.H. Sherman "Review of Literature Related to Residential Ventilation Requirements," June 2005. LBNL-57236. <http://epb.lbl.gov/Publications/lbnl-57236.pdf>
#### Abstract
This paper reviews current ventilation codes and standards for residential buildings in Europe and North America. It also examines the literature related to these standards such as occupant surveys of attitudes and behavior related to ventilation, and research papers that form the technical basis of the ventilation requirements in the standards. The major findings from the literature are that ventilation is increasingly becoming recognized as an important component of a healthy dwelling, that the ventilation standards tend to cluster around common values for recommended ventilation rates, and that surveys of occupants showed that people generally think that ventilation is important, but that their understanding of the ventilation systems in their houses is low.
Russell, M, M.H. Sherman and A. Rudd "Review of Residential Ventilation Technologies," August 2005. LBNL-57730. <http://epb.lbl.gov/Publications/lbnl-57730.pdf>
#### Abstract
This paper reviews current and potential ventilation technologies for residential buildings with particular emphasis on North American climates and construction. The major technologies reviewed include a variety of mechanical systems, natural ventilation, and passive ventilation. Key parameters that are related to each system include operating costs, installation costs, ventilation rates, and heat recovery potential. It also examines related issues such as infiltration, duct systems, filtration options, noise, and construction issues. This report describes a wide variety of systems currently on the market that can be used to meet ASHRAE Standard 62.2-2004. While these systems generally fall into the categories of supply, exhaust or balanced, the specifics of each system are driven by concerns that extend beyond those in the standard and are discussed. Some of these systems go beyond the current standard by providing additional features (such as air distribution or pressurization control). The market will decide the immediate value of such features, but ASHRAE may wish to consider related modifications to the standard in the future.
The second report was accepted as an ASHRAE Research Journal article. The Abstracts are reproduced here in this section. The full texts are provided as attachments to this final report.
### **2\. Summary of Simulation Plan (Task 2)**
Using the results of the Task 1 Literature Review, a detailed plan was made for conducting simulations and analyses of the performance of whole-house mechanical ventilation systems in new residential buildings. The simulation plan specified the key variables to be studied and defined the criteria to be used in the analysis. Key variables included: ventilation system type and controls; a full range of climate zones, seasons and peak weather; and building description details such as physical properties, operating schedules, internal heat gain rates, and occupancy. As part of the development of this plan, the project team presented to and received input from the ASHRAE SSPC 62.2 and participants of a DOE Building America Ventilation Expert meeting.
The plan was submitted to the ARTI project monitoring subgroup (PMS) and approved prior to proceeding with the Task 3 Simulation and Analysis. However, in the course of analyzing the simulation results, a number of questions arose illuminating areas where the Simulation Plan fell short, necessitating adjustment of some inputs and assumptions. These changes were also presented to and approved by the PMS. In addition, the PMS requested a several changes: 1) changing to the reference house from a leaky house to a house with the same tighter envelope as the mechanically ventilated houses, 2) doing detailed humidity calculations in all climates, and 3) expanding HRV/ERV simulations to more climates.
The final Simulation Plan is reproduced here in part for clarity because of the revisions, and to more conveniently assist the reader in interpreting the Simulation and Analysis results of Task 3. Appendix I of the Simulation Plan, which provides the details the REGCAP simulation, REGCAP, is included as Appendix D to this report.
#### Introduction
This simulation plan outlines the pertinent ASHRAE Standard 62.2 requirements that will be simulated using different ventilation technologies. The information required to simulate each approach is summarized together with rationales for selection of particular parameters. The technologies are discussed in more detail in the companion Ventilation Technologies Review report.
The HVI Directory1 was used to obtain fan power for fans that met the airflow and sound requirements of ASHRAE Standard 62.2 In this plan the specific fan manufacturers and model numbers are given in square parentheses [] for each system.
Approximately 100 different combinations of house size, climate and ventilation technologies will be simulated in all. The REGCAP2 simulation model will be used to perform minute-by-minute simulations combined with post-processing to answer keyquestions. The REGCAP model has been used in several previous studies looking at HVAC system performance3. REGCAP has a detailed airflow network model thatcalculates the airflow through building components as they change with weather conditions and HVAC system operation. The airflows include the effects of weather and leak location, and the interactions of HVAC system flows with house and attic envelopes. These airflow interactions are particularly important because the airflows associated with ventilation systems (including duct leakage) interact significantly with the effects of natural infiltration in houses.
Because REGCAP performs minute by minute simulations, the dynamic effects of HVAC systems are captured. This includes issues of cyclic duct losses and latent capacity of air conditioners.
#### Houses to be simulated
Three house sizes will be simulated to examine the implicit effect of occupant density in the ASHRAE Standard 62.2 requirements. For most of the simulations the medium sized house will be used, and for selected cases smaller and larger houses will be simulated.
  1. Small 1000 ft2 2 bedroom Bungalow.
  2. Mid-size 2000 ft2, 2 story, 3 bedrooms
  3. Large 4000 ft2 2-story, 5 bedrooms.


Two levels of envelope leakage will be examined. The high leakage values in Table 2.4 will be used as a “non-mechanically ventilated ASHRAE Standard 62.2 compliant house”. (In the original simulation plan this was to be the reference house.) For the mechanical ventilation simulations, the envelopes will be tighter. The tighter envelope will also be used for a set of simulations with no ASHRAE Standard 62.2 compliant mechanical ventilation. This tight but unventilated house will be used as a basis of comparison for the other simulations. From the LBNL air leakage database for typical new construction4 the Normalized Leakage is NL=0.3 (or about 6 ACH50). The corresponding leakage values are summarized in Table 2.1.
**Table 2.1** Envelope Leakage for Mechanically Ventilated Homes
Floor area (ft2)| ACH 50| ELA4 (in2)| m3/sPan| cfm/Pan  
---|---|---|---|---  
1000| 5.8| 43| 0.028| 61  
2000| 5.8| 86| 0.057| 121  
4000| 5.8| 173| 0.114| 243  
Building insulation and duct system parameters used to determine the non-ventilation building load will vary by climate as shown in Table 2.2. The envelope characteristics are based on a house that meets IECC requirements and are referred to as the Standard-Performance houses. Exterior surface area for wall insulation scales with floor area and number of stories. The surface area is typically three times the floor area (based on the BSC/Building America data set). Window area is 18% of floor area with windows equally distributed in walls facing in the four cardinal directions.
#### Higher-Performance Houses
Simulation of higher-performance houses broadens the application of the results for above-code programs such as the USDOE Building America Program. The higherperformance houses will be simulated for all medium house size cases. The differences between the higher-performance and standard-performance houses are:
  * Tighter envelopes. The higher-performance houses have half the envelope leakage.
  * All ducts inside conditioned space
  * Glazing has U=0.35 and SHGC=0.35. It should be noted that in some heating dominated climates, the lower SHGC can increase heating load more than it reduces cooling load.
  * Changed thermostat to be constant setpoint: 76°F cooling, 70°F heating
  * Changed heating and cooling capacities to match ACCA Manual J loads. . . 


Download complete report [here](/file/3177).
**Footnotes:**
  1. HVI. 2005. Certified Home Ventilating Products Directory, Home Ventilating Institute.
  2. Appendix D gives details of the simulation model.
  3. See REGCAP Bibliography at the end of Appendix D.
  4. Sherman, M.H. and Matson, N.E.,"Air Tightness of New U.S. Houses: A Preliminary Report ", Lawrence Berkeley National Laboratory, LBNL-48671, 2002