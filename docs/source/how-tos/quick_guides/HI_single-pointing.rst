############################################
How to observe an HI spectrum and process it
############################################


The instructions below will run you through the steps required to setup your observing scripts to execute an HI pointed observation (using either frequency- or position-switching) and how to reduce the data.


Observing Script
================

At the GBT we use AstrID to prepare and execute scheduling blocks.  However the following can be created using any standard simple text editing tool, and then copied over to the astrid screen.  

Catalog
-------
Before you start writing your scheduling block it is helpful to prepare a source catalog in a separate file. This is especially advised if you have a long list of sources. For a short catalog it is also possible to add the sources directly in your scheduling block (not described here). 

To find out more about catalogs: GBT Observer's Guide: Section 6.3

Catalogs should be stored in the project directory (/home/astro-util/projects/your project directory/).  
For examples "quickguides", so these scripts are available in /home/astro-util/projects/quickguides).
Catalogs are typically names "XXX.cat.  The catalog below is "qg_HI.cat"

Here is an example of a RA/Dec coordinate system catalog with velocity:

.. code-block:: python

    # Source List for HI observing with RA/Dec coordinates.

    coordmode= j2000
    head = name      ra          dec        velocity             
    RSCG31   09:17:26.5     41:57:18        1600
    RSCG64   12:41:33.2     26:03:56        4800
    GalaxyX  02:53:41.3    +13:00:52.9      0          

Format tells the catalog this is a set of source with a fixed position in one of our standard coordinate systems, e.g., RA/DEC, AZ/EL,
GLON/GLAT, etc. The other options are for rapidly moving objects, such as planets, asteroids, etc.

Coordmode is the ephemeris date for the coordinates

RA/DEC are one set of coordinate options (instead of, e.g. GLONG/GLAT). 

VEL is source velocity in units of km/s. The reference frame is set using the VDEF keyword in the config. This is used to shift the center of the observing bands using the defined (in the config tool) reference frame.

You can also include any number of user defined keywords. These can be useful for reference and/or for making more complicated scripts.  oSee Observer’s guide for more information.

We advise to save this catalog as a ‘.cat’ file, in a known location (Should this be the standard project directory instead??). We will call it later from our scheduling block(s).



Configuration
-------------

The next step is to determine the hardware configuration you desire.  This can be a bit confusing, but below are three options that you can use/modify.
These configurations can be saved directly in your astrid script.  We commonly name the cnofigurations, to make the astrid scripts easily readable.  This has 
been done for these configurations ("psw_HI_config_known" "psw_HI_config_unknown"  and "fsw_HI_config").

.. tab:: Position-switching (psw) - known velocity

    .. code-block:: python

        # Configuration parameters for spectral line observations of HI using position switching, where the source velocity is known
        # This is set up for determining the HI content of a galaxy with a known velocity
        # Here we are using VEGAS mode 18, but using only one of the eight VEGAS banks
        # Here we have only one, 11.72 MHz wide, band which will be centered at the frequency of the galaxy's HI.
        # We will observe with two linear polarizations, and will sum those polarizations during the data reduction phase.
        # Observations will be taken as 5 minutes on and 5 minutes off, with the off source observation covering the same aziuth and elevation as the on.
        # The observation period (tint) is set to 6s.  As there are only two phases (cal on, cal off), the data will be written to disk once every 3 second (tint/# of phases)

        psw_HI_config_known='''
        receiver        = 'Rcvr1_2'         # Specifies L-Band receiver, used for most HI observations
        obstype         = 'Spectroscopy'    # Specifies spectral line observations (required for spectral line observations)
        backend         = 'VEGAS'           # Specifies spectral line backend (required for spectral line observations)
        restfreq        = 1420.4058         # Specifies rest frequency for HI (MHz);  Used for shifting the center of the bands to the correct, redshifted velocities
        deltafreq       = 0.0               # Specifies offsets for each spectral window (MHz).    
        bandwidth       = 11.72             # Defined by chosen VEGAS mode (MHz)
        nchan           = 262144            # Specifies number of channels in spectral window
        vegas.subband   = 1                 # Specifies single or multiple spectral windows (1 or 8)
        swmode          = 'tp'              # Specifies switching mode, switching power with noise diode
        swtype          = None              # Specifies type of switching, no switching
        swper           = 1.0               # Specifies length of full switching cycle (seconds)
        swfreq          = 0, 0              # Specifies frequency offset (MHz)
        tint            = 6.0               # Specifies integration time (sec; integer multiple of swper)
        vframe          = 'lsrk'            # Specifies velocity reference frame
        vdef            = 'Optical'         # Specifies Doppler-shifted velocity frame
        noisecal        = 'lo'              # Specifies level of the noise diode, use ‘lo’ for most observations
        pol             = 'Linear'          # Specifies ‘Linear’ or ‘Circular’ polarization
        notchfilter     = 'In'              # Specify ‘In’ to block 1200-1310 MHz RFI signal
        '''

.. tab:: Position-switching (psw) - unknown velocity

    .. code-block:: python

        # Configuration parameters for spectral line observations of HI using position switching, where the source velocity is not known (velocity=0)
        # This is set up for searching for the HI  of a galaxy without a known velocity
        # This is using VEGAS mode #18
        # Here we have 8 x 11.72 MHz wide banks overlapping by 1.72 MHz, which will cover the velocity range 1340.4058-1422.1258.
        # We will observe with two linear polarizations, and will sum those polarizations during the data reduction phase.
        # Observations will be taken as 5 minutes on and 5 minutes off, with the off source observation covering the same aziuth and elevation as the on.
        # The observation period (tint) is set to 6s.  As there are only two phases (cal on, cal off), the data will be written to disk once every 3 second (tint/# of phases)

        psw_HI_config_unknown='''
        receiver        = 'Rcvr1_2'        # Specifies L-Band receiver, used for most HI observations
        obstype         = 'Spectroscopy'   # Specifies spectral line observations (required for spectral line observations)
        backend         = 'VEGAS'          # Specifies spectral line backend (required for spectral line observations)
        restfreq        = 1420.4058        # Specifies rest frequency for HI (MHz);  Used for shifting the center of the bands to the correct, redshifted velocities in chosen referenc eframe
        deltafreq       = -10.0,-20.0,-30.0,-40.0,-50.0,-60.0,-70.0,-80.0   # Specifies offsets for each spectral window (MHz).    
        bandwidth       = 11.72             # Defined by chosen VEGAS mode (MHz)
        nchan           = 262144            # Specifies number of channels in spectral window
        vegas.subband   = 1                 # Specifies single or multiple spectral windows for each VEGAS band (1 or 8)
        swmode          = 'tp'              # Specifies switching mode, switching power with noise diode
        swtype          = None              # Specifies type of switching, no switching
        swper           = 1.0               # Specifies length of full switching cycle (seconds)
        swfreq          = 0, 0              # Specifies frequency offset (MHz)
        tint            = 6.0               # Specifies integration time (sec; integer multiple of swper)
        vframe          = 'lsrk'            # Specifies velocity reference frame
        vdef            = 'Optical'         # Specifies Doppler-shifted velocity frame
        noisecal        = 'lo'              # Specifies level of the noise diode, use ‘lo’ for most observations
        pol             = 'Linear'          # Specifies ‘Linear’ or ‘Circular’ polarization
        notchfilter     = 'In'              # Specify ‘In’ to block 1200-1310 MHz RFI signal
        '''
.. tab:: Frequency-switching (fsw)

    .. code-block:: python
        
        # Configuration parameters for spectral line observations of HI using frequency switching.
        # This is set up for determining the HI content of a galaxy with a known velocity
        # Here we are using VEGAS mode 18, but using only one of the eight VEGAS banks
        # Here we have only one, 11.72 MHz wide, band which will be centered at the frequency of the galaxy's HI.
        # The frequency switching will be set to be +/- 2.5 MHz
        # We will observe with two linear polarizations, and will sum those polarizations during the data reduction phase.
        # The observation period (tint) is set to 6s.  As there are four two phases (cal on & freq1, cal off & freq1, cal on & freq2,cal off & freq2), the data will be written to disk once every 1.5 seconds (tint/# of phases)

        fsw_HI_config='''
        receiver        = 'Rcvr1_2'         # Specifies L-Band receiver for HI
        obstype         = 'Spectroscopy'    # Specifies spectral line observations
        backend         = 'VEGAS'           # Specifies spectral line backend
        restfreq        = 1420.4058         # Specifies rest frequency for HI (MHz)
        deltafreq       = 0.0               # Specifies offsets for each spectral window (MHz)
        bandwidth       = 11.72             # Defined by chosen VEGAS mode (MHz)
        nchan           = 262144             # Specifies number of channels in spectral window
        vegas.subband   = 1                 # Specifies single or multiple spectral windows (1 or 8)
        swmode          = 'sp'              # Specifies switching mode, switching power with noise diode
        swtype          = 'fsw'             # Specifies type of switching, no switching
        swper           = 1.0               # Specifies length of full switching cycle (seconds)
        swfreq          = 2.50, -2.50       # Specifies frequency offset (MHz)
        tint            = 6.0               # Specifies integration time (sec; integer multiple of swper)
        vframe          = 'lsrk'            # Specifies velocity reference frame
        vdef            = 'Optical'         # Specifies Doppler-shifted velocity frame
        noisecal        = 'lo'              # Specifies level of the noise diode, use ‘lo’ for ‘fsw’
        pol             = 'Linear'          # Specifies ‘Linear’ or ‘Circular’ polarization
        notchfilter     = 'In'              # Specify ‘In’ to block 1200-1310 MHz RFI signal
        '''

.. note::	   
    Your parameters may differ based on your specific science goals.


Scheduling Block(s)
-------------------

To find out more about scripts: GBT Observer's Guide: Section 6.1

AstrID is used to submit scheduling blocks for GBT observations. Astrid is python-based and can incorporate custom user scripts. Here is an example of a basic position switched, tracking observation for HI observing, using the catalog and configurations from above.


.. tab:: Position-switching (psw)

    .. code-block:: python

        # Observing script for spectral line observations of HI using position switching.

        # Reset configuration from prior observation.  This is important
        ResetConfig()

        # Import catalog of flux calibrators and standard HI sources, for calibration and quick checks.
        Catalog(fluxcal)
        Catalog('/home/astro-util/astridcats/HI_strong.cat')

        # Import catalog created above, with your sources
        Catalog('/home/astro-util/projects/quick_guide/catalogs/qg_HI.cat')

        # Define configuration parameters;  this is just a copy of the psw_HI_config_known configuration, above.
        psw_HI_config_known='''
        receiver        = 'Rcvr1_2'         
        obstype         = 'Spectroscopy'    
        backend         = 'VEGAS'           
        restfreq        = 1420.4058         
        deltafreq       = 0.0                
        bandwidth       = 11.72             
        nchan           = 262144            
        vegas.subband   = 1                 
        swmode          = 'tp'              
        swtype          = None             
        swper           = 1.0             
        swfreq          = 0, 0           
        tint            = 6.0              
        vframe          = 'lsrk'            
        vdef            = 'Optical'        
        noisecal        = 'lo'              
        pol             = 'Linear'          
        notchfilter     = 'In'             
        '''

        # Configure telescope.  The ensures the correc receiver is in place for the peak calibration scan
        Configure(psw_HI_config_known)

        # Slew the telescope to your source of interest
        Slew('RSCG64')

        # Perform pointing correction on calibrator near your source of interest.
        AutoPeak()

        # Slew to your source from the standard catalog, to sanity check your observations
        Slew('U7766')

        # Reconfigure after calibrator corrections.
        Configure(psw_HI_config)

        # Balance the IF system.
        Balance()

        # OffOn produces two scans each of the specified duration (in seconds) which tell the GBT to take data for 10 minutes.
        # Here, the offset is designed to cover the same azimuth and elevation as the source, which provides the optimum baseline removal.

        OnOff('U7766', Offset('J2000', '-00:05:00', 0.0, cosv=True), 300)

        # Now lets go to the main object of interest
        Slew('RSCG64')

        #Again, balance the power levels
        Balance()

        # In this case, lets get 8 on+off observations of the object;  this will take about 44 minutes.

        obs_loop=0
        while obs_loop <8:
            OnOff('RSCG64', Offset('J2000', '-00:05:00', 0.0, cosv=True), 300)
            obs_loop += 1


.. tab:: Frequency-switching (fsw)

    .. code-block:: python

        # Observing script for spectral line observations of HI using frequency-switching.

        # Reset configuration from prior observation.
        ResetConfig()

        # Import catalog of flux calibrators and standard HI sources, for calibration and quick checks.
        Catalog(fluxcal)
        Catalog('/home/astro-util/astridcats/HI_strong.cat')

        # Import catalog created above, with your sources
        Catalog('/home/astro-util/projects/quick_guide/catalogs/qg_HI.cat')

        # Define configuration parameters
        fsw_HI_config='''
        receiver        = 'Rcvr1_2'         
        obstype         = 'Spectroscopy'    
        backend         = 'VEGAS'           
        restfreq        = 1420.4058         
        deltafreq       = 0.0               
        bandwidth       = 11.72             
        nchan           = 262144           
        vegas.subband   = 1                 
        swmode          = 'sp'              
        swtype          = 'fsw'             
        swper           = 1.0               
        swfreq          = 2.50, -2.50       
        tint            = 6.0               
        vframe          = 'lsrk'            
        vdef            = 'Optical'         
        noisecal        = 'lo'              
        pol             = 'Linear'          
        notchfilter     = 'In'              
        '''

        # Configure telescope.
        Configure(fsw_HI_config)

        # This time, you've chsen the calibrator you wish to use.  So first, slew to it
        # Slew to your source or calibrator.
        Slew('3C196')

        # Perform pointing correction on nearby calibrator.
        AutoPeak('3C196')

        # Slew to your source from the standard catalog, to sanity check your observations
        Slew('U7766')

        # Reconfigure after calibrator corrections.
        Configure(fsw_HI_config)

        # Balance the hardware.
        Balance()

        # As you are frequency switching, this time you just want to track your obect.  Here, again, we will run a 5 minute observation
        # Note that the "None" tells the telescope to stay on the soure, and not to drive to a new, offset, location.
        Track('U7766',None,300)

        # Now, slew to your source.
        Slew('RSCG31')

        # Balance the hardware.
        Balance()

        # Observe your source!
        Track('RSCG31',None,300)



Data Reduction
==============

To find out more about data reduction: GBTIDL User's Guide

.. todo::
    
    Add GBTIDL API in references and then link properly.



Our current data reduction routines are written in IDL. Users can build custom scripts incorporating generic IDL commands. We will run through some common GBT IDL commands below. From the Green Bank Observatory data reduction machine arcturus, start GBTIDL by typing in a terminal

.. code-block:: bash
   
    gbtidl


Position-switched spectra
-------------------------

.. admonition:: Data

    TGBT20A_506_01


.. todo::
    
    Make sure this is the right data directory.



To access test the data presented in this reference guide type ‘offline’ followed by the project name: 

.. code-block:: idl

    offline, "TGBT20A_506_01"


‘Connecting to file’ tells you where the raw data files are located. File updated shows how long ago the last scan was updated.
   

.. note::

    To view data from a different observing project, replace the (TGBT20A_506_01) with the information for your project:
        - Semester number (e.g., AGBT20A)
        - Project number (e.g., 108)
        - Session number (e.g., 01)

    To access current observations, or see real-time data during an observing session, type 'online' from the command line. The project code is not needed in online mode.


View a summary of the observations:

.. code-block:: idl

   summary


.. todo:: 

    Add screenshot of the output here.


For more information on what each column is, please see the GBTIDL User’s Guide GBTIDL User's Guide: Section 4.7.


To view the position-switched observations type

.. code-block:: idl

   getps, 6


.. image:: images/HI-psw-sp__gbtidl_01.png 
  
You can change the x-axis to the Doppler shifted velocity of the rest frequency (F0) by clicking on the 'GHz' GUI button and selecting 'km/s'.    

To get the second polarization, type

.. code-block:: idl

   getps, 6, plnum=1

To stack/average multiple scans together to improve signal to noise in the spectrum type

.. code-block:: idl

   getps, 6
   accum
   getps, 8
   accum
   ave

To smooth your spectra by a specific number of channels, you can use the ‘gsmooth’ command:

.. code-block:: idl

   getps, 6
   gsmooth, 5


.. image:: images/HI-psw-sp__gbtidl_02.png


You can do all this for the second source as well.

.. note::

    If you have multiple IF tunings, you may view those other IFs by indicating ifnum=0, 1, 2, etc.

Saving and/or exporting your data can be done in multiple ways.  All of these procedures are located in the GBTIDL User's Guide: Section 9. One way to write a spectrum to file is using

.. code-block:: idl

    write_ascii, "mydata.txt"

This will write the spectrum into a file called "mydata.txt" into the current directory.


Frequency-switched spectra
--------------------------

.. admonition:: Data

    TGBT20A_506_02


.. todo::
    
    Make sure this is the right data directory.



To access test the data presented in this reference guide type ‘offline’ followed by the project name: 

.. code-block:: idl

    offline, "TGBT20A_506_02"


‘Connecting to file’ tells you where the raw data files are located. File updated shows how long ago the last scan was updated.
   

.. note::

    To view data from a different observing project, replace the (TGBT20A_506_02) with the information for your project: 
        - Semester number (e.g., AGBT20A)
        - Project number (e.g., 108)
        - Session number (e.g., 01)

    To access current observations, or see real-time data during an observing session, type 'online' from the command line. The project code is not needed in online mode.


View a summary of the observations:

.. code-block:: idl

   summary


.. todo:: 

    Add screenshot of the output here.


For more information on what each column is, please see the GBTIDL User’s Guide GBTIDL User's Guide: Section 4.7.


To view the position-switched observations type

.. code-block:: idl

   getfs, 6


.. todo::

    Add screenshot


You can change the x-axis to the Doppler shifted velocity of the rest frequency (F0) by clicking on the 'GHz' GUI button and selecting 'km/s'.    

To get the second polarization, type

.. code-block:: idl

   getfs, 6, plnum=1

To stack/average multiple scans together to improve signal to noise in the spectrum type

.. code-block:: idl

   getfs, 6
   accum
   getfs, 8
   accum
   ave

To smooth your spectra by a specific number of channels, you can use the ‘gsmooth’ command:

.. code-block:: idl

   getfs, 6
   gsmooth, 5


.. todo::
   
   Add screenshot.


You can do all this for the second source as well.

.. note::

    If you have multiple IF tunings, you may view those other IFs by indicating ifnum=0, 1, 2, etc.

Saving and/or exporting your data can be done in multiple ways.  All of these procedures are located in the GBTIDL User's Guide: Section 9. One way to write a spectrum to file is using

.. code-block:: idl

    write_ascii, "mydata.txt"

This will write the spectrum into a file called "mydata.txt" into the current directory.
