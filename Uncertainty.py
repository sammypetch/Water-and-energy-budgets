
def basin_error(C, b, F , F_error):
    '''
    calculates basin uncertainty by downscaling continental uncertainties using assosiated areas.
    
    C = continent number, see key 1 to 4
    NA = 1, SA = 2 ,EA = 3, AF = 4
    
    B = basin number
    enter basin id number from 1-28
    
    select flux
    F = i.e one of {P, Q, LE, DSR, DLR, USW, ULW, SH}
    
    F_error = i.e {P_error, Q_error ..} uncertainties from NEWS.  

    '''
    
    C_area =  Area_cont[C-1] # continent area
    B_area = Basin_areas[b-1] # basin area 
    
    cont_flux = mask_continent(F,C)
    
    clat_C = mask_continent2d(clat2D,C) # cosine latitude 
    weighted_cont_flux = np.zeros(12)
    for i in range(12):
        weighted_cont_flux[i] = (C_flux[i,:,:]*clat_C).sum()/(clat_C).sum()
        
    cont_flux = weighted_cont_flux
    basin_flux = mm_w_array(mask_data(F,b),b)) # monthly mean weaighted array of basin flux
   
    error = np.zeros(12)
    for i in range(12):
        error[i] = np.sqrt((basin_flux[i]/cont_flux[i])/(B_area/C_area))*cont_error[i] 
    return error



Area_name = ['North America', 'South America', 'Eurasia', 'Africa']
Area_cont =[24030089, 17737690, 53234055, 29903956] # area in km^2

Basin_areas = [5853804,3826122,3698802.75,3202958.75,2902864.5,2661391.75 
,2582221,2570130.5,2417937.25,2240018.75,1988755.75,1818799.375,1794242.5
,1712738.25,1628404.5,1571536,1463314.75,1266641.75,1143101.125,
1070229.875,1047385.687,1039361.750,1031512.062,977516.437,967340.562,
943577.187,893627.312]


lat_rad = b_lat*np.pi/180 # convert latitude to radians
cos_lat = np.cos(lat_rad) # coaine latitude for weighting data 
lons2D, clat2D = np.meshgrid(b_lon,cos_lat)

# example for Amazon basin 
Perror = basin_error(2, 1 , P, PNEWS_error) 
Qerror = basin_Error(2,1, Q, QNEWS_error) 
