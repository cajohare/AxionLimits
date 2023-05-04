#================================PlotFuncs_ScalarVector.py==================================#
# Created by Ciaran O'Hare 2022

# Description:
# This file has some extra classes for dealing with the scalar and vector plots 
# only

#==============================================================================#

from PlotFuncs import *

def NaturalnessCorner(ax,scale,Lambda_min_TeV,dim,edgecolor='gold',facecolor='gold',
                      lw=3,path_effects=line_background(4,'k'),
                      nlevels=100,alpha=0.1,Lambda_max_TeV=1e20,
                      mass_label=5e-13,
                     text_label=r'Natural $d_e$ ($\Lambda = 10$ TeV)',
                     text_shift=[1,1],zorder=-100,
                     Shading=True,fs=25):
    m_vals = array([1e-30,1e30])
    d_natural = lambda m,Lambda : m/(scale*Lambda**dim)
    ax.plot(m_vals,d_natural(m_vals,Lambda_min_TeV*1e12),'-',lw=lw,color=edgecolor,path_effects=path_effects,zorder=zorder)
   
    if Shading:
        Lambda_vals = logspace(log10(Lambda_min_TeV),log10(Lambda_max_TeV),nlevels)
        for Lambda in Lambda_vals:
            ax.fill_between(m_vals,d_natural(m_vals,Lambda*1e12),y2=1e-100,color=facecolor,alpha=alpha,zorder=zorder,lw=0)
  
    trans_angle = plt.gca().transData.transform_angles(array((45.0,)),array([[0, 0]]))[0]
    ax.text(mass_label*text_shift[0],0.1*d_natural(mass_label,Lambda_min_TeV*1e12)*text_shift[1],text_label,fontsize=fs,color=edgecolor,rotation=trans_angle,path_effects=line_background(1,'k'),clip_on=True,zorder=zorder)
    return
    
def FuzzyDM(ax,edgecolor='#205e8a',facecolor='#205e8a',text_col='#205e8a',
                      lw=3,path_effects=line_background(0,'k'),
                      nlevels=100,alpha=0.05,m_max=2e-20,m_min=1e-24,
                      g_label=5e-13,fs=23,
                     text_label=r'{\bf Structure formation}',
                     text_shift=[1,1],zorder=-100,rotation=90,
                     ymax=1e30,ymin=1e-30):
    g_vals = array([ymin,ymax])
    m_vals = logspace(log10(m_min),log10(m_max),nlevels)
    for m in m_vals:
        ax.fill_between(array([1e-30,m]),array([ymax,ymax]),y2=ymin,color=facecolor,alpha=alpha,zorder=zorder,lw=0)
    ax.text(m_max*text_shift[0]*0.5,g_label*text_shift[1],text_label,fontsize=fs,color=text_col,rotation=rotation,path_effects=line_background(1,'k'),clip_on=True,zorder=zorder)
    return


class ScalarPhoton():
    def MICROSCOPE(ax,text_label=r'{\bf MICROSCOPE}',text_pos=[1e-16,0.34e-3],col='#84878c',text_col='k',fs=15,zorder=-1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/MICROSCOPE.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def EotWashEP(ax,text_label=r'{\bf E\"ot-Wash (EP)}',text_pos=[1.4e-24,1.8e-3],col='gray',text_col='k',fs=20,zorder=0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/EotWashEP.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def FifthForce(ax,text_label=r'{\bf Fifth force (ISL)}',text_pos=[0.5e-21,0.6e2],rotation=-25,col='darkgray',text_col='k',fs=20,zorder=0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/FifthForce.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def GlobularClusters(ax,text_label=r'{\bf Globular clusters}',text_pos=[2e-24,3.3e9],col=[0.0, 0.66, 0.42],text_col='w',fs=27,zorder=1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/GlobularClusters.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def AURIGA(ax,text_label=r'{\bf AURIGA}',text_pos=[0.18e-11,0.1e-6],rotation=90,col='darkred',text_col='darkred',fs=17,zorder=0.0,text_on=True,Projection=False,edgealpha=1,lw=0):
        dat = loadtxt("limit_data/ScalarPhoton/AURIGA.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def DyDy(ax,text_label=r'{\bf Dy/Dy}',text_pos=[0.4e-22,0.3e-6],rotation=28,col='#a11a4e',text_col='w',fs=19,zorder=0.02,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/DyDy.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def DyQuartz(ax,text_label=r'{\bf Dy/Quartz}',text_pos=[0.1e-15,3e-1],rotation=28,col='#c11a4e',text_col='w',fs=20,zorder=0.10,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/DyQuartz.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return


    def YbSr(ax,text_label=r'{\bf Yb$^+$/Sr}',text_pos=[2e-20,1.5e-6],rotation=23,col='#a11b33',text_col='w',fs=15,zorder=0.0,text_on=True,Projection=False,edgealpha=1,lw=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/ScalarPhoton/YbSr.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=path_effects)
        return

    
    def RbCs(ax,text_label=r'\center{{\bf SYRTE \newline Rb/Cs}}',text_pos=[0.25e-23,4e-7],rotation=-30,col='#c7345d',text_col='w',fs=17,zorder=0.01,text_on=True,Projection=False,edgealpha=1,lw=1):
        dat = loadtxt("limit_data/ScalarPhoton/RbCs.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1,'k'))
        return
    
    def BACON(ax,text_label=r'{\bf BACON}',text_pos=[0.1e-21,0.075e-7],rotation=26,col='#59042d',text_col='#59042d',fs=18,zorder=0.0,text_on=True,Projection=False,edgealpha=1,lw=1):
        dat = loadtxt("limit_data/ScalarPhoton/BACON.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def PTB(ax,text_label=r'{\bf PTB}',text_pos=[0.3e-20,1.2e-8],rotation=23,col='#d11b33',text_col='#d11b33',fs=19,zorder=-0.01,text_on=True,Projection=False,edgealpha=1,lw=1):
        dat = loadtxt("limit_data/ScalarPhoton/PTB.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def SrSi(ax,text_label=r'{\bf Sr/Si}',text_pos=[0.3e-17,0.4e-3],rotation=13,col='#730f3a',text_col='w',fs=14,zorder=0.0,text_on=True,Projection=False,edgealpha=1,lw=1):
        dat = loadtxt("limit_data/ScalarPhoton/SrSi.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def HQuartzSapphire(ax,text_label=r'\center{\bf H/Quartz/Sapphire}',text_pos=[0.7e-18,1e4],rotation=0,col='#a81313',text_col='w',fs=20,zorder=0.11,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/HQuartzSapphire.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def I2(ax,text_label=r'{\bf I}$_2$',text_pos=[0.5e-12,1e6],rotation=0,col='#b52452',text_col='w',fs=25,zorder=0.13,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/I2.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def DAMNED(ax,text_label=r'{\bf DAMNED}',text_pos=[0.85e-10,0.7e4],rotation=90,col='#b5243f',text_col='w',fs=13,zorder=0.11,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/DAMNED.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    
    def GEO600(ax,text_label=r'{\bf GEO600}',text_pos=[4e-13,1e2],rotation=0,col='#b5260d',text_col='w',fs=20,zorder=0.11,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/GEO600.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def LIGO(ax,text_label=r'{\bf LIGO}',text_pos=[0.53e-13,0.15e3],rotation=90,col='#c3151d',text_col='w',fs=15,zorder=0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/LIGO.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

        
    def Holometer(ax,text_label=r'{\bf Holometer}',text_pos=[1.85e-10,0.15e9],rotation=0,col='#b53724',text_col='w',fs=15,zorder=0.17,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/Holometer.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1,'k'))
        return
    
            
    def DynamicDecoupling(ax,text_label=r'\center{\bf Dynamic \newline decoupling}',text_pos=[0.8e-13,0.15e9],rotation=-26,col='crimson',text_col='w',fs=10,zorder=0.14,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/DynamicDecoupling.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1,'k'))
        return

        
    def CsCav(ax,text_label=r'{\bf Cs/Cav}',text_pos=[3e-8,0.2e7],rotation=55,col='red',text_col='w',fs=18,zorder=0.109,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/CsCav.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    # Projected
    def AEDGE(ax,text_label=r'{\bf AEDGE}',text_pos=[1e-16,0.1e-11],rotation=50,col='#eb4034',text_col='#eb4034',fs=20,zorder=-1.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/Projections/AEDGE.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
        
    def AION(ax,text_label=r'{\bf AION}',text_pos=[1e-14,6e-7],rotation=51,col='#eb4034',text_col='#eb4034',fs=18,zorder=-1.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/Projections/AION-km.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def MAGIS(ax,text_label=r'{\bf MAGIS}',text_pos=[4e-16,2e-7],rotation=35,col='#eb4034',text_col='#eb4034',fs=17,zorder=-1.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/Projections/MAGIS-km.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def NuclearClock(ax,text_label=r'{\bf Nuclear clock}',text_pos=[2e-19,2e-12],rotation=30,col='darkred',text_col='darkred',fs=20,zorder=-1.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/Projections/NuclearClock.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def DUAL(ax,text_label=r'{\bf DUAL}',text_pos=[0.5e-11,1e-6],rotation=0,col='#a10649',text_col='#a10649',fs=15,zorder=0,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/Projections/DUAL.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def FOCOS(ax,text_label=r'{\bf FOCOS}',text_pos=[9e-17,3e-5],rotation=0,col='gray',text_col='gray',fs=17,zorder=-1.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/Projections/FOCOS.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
        

    def Resonators(ax,text_label=r'{\bf Resonators}',ms=7,alpha=0.75,text_pos=[0.1e-9,0.9e-4],rotation=23,rotation2=90,col='#690c43',text_col='#690c43',fs=25,fs2=13,zorder=0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarPhoton/Projections/Resonator-Sapphire.txt")
        plt.plot(dat[:-15,0],dat[:-15,1],'--',color=col,zorder=zorder,alpha=alpha,lw=lw)
        dat = loadtxt("limit_data/ScalarPhoton/Projections/Resonator-Pillar.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=zorder,alpha=alpha,lw=lw)
        dat = loadtxt("limit_data/ScalarPhoton/Projections/Resonator-Quartz.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=zorder,alpha=alpha,lw=lw)
        dat = loadtxt("limit_data/ScalarPhoton/Projections/Resonator-Helium.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=zorder,alpha=alpha,lw=lw)

        ax.text(1.8e-11,3e-2,'Helium',rotation=rotation2,fontsize=fs2,color=text_col,alpha=alpha)
        ax.text(1.3e-10,3e-2,'Sapphire',rotation=rotation2,fontsize=fs2,color=text_col,alpha=alpha)
        ax.text(4e-9,0.7e-1,'Pillar',rotation=rotation2,fontsize=fs2,color=text_col,alpha=alpha)
        ax.text(4.5e-7,0.8e2,'Quartz BAW',rotation=rotation2,fontsize=fs2,color=text_col,alpha=alpha)
        plt.text(text_pos[0],text_pos[1],text_label,rotation=rotation,color=text_col,fontsize=fs,alpha=alpha)

        return

class ScalarElectron():
    
    def MICROSCOPE(ax,text_label=r'{\bf MICROSCOPE}',text_pos=[2e-24,6e-3],col='#84878c',text_col='k',fs=20,zorder=0.0,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/MICROSCOPE.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def EotWashEP(ax,text_label=r'{\bf E\"ot-Wash (EP)}',text_pos=[2e-24,0.8e-1],col='gray',text_col='k',fs=20,zorder=0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/EotWashEP.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
        
    def FifthForce(ax,text_label=r'{\bf Fifth force (ISL)}',text_pos=[0.5e-21,4e2],rotation=-26,col='darkgray',text_col='k',fs=20,zorder=0.101,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/FifthForce.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def RedGiants(ax,text_label=r'{\bf Red giants}',text_pos=[2e-24,7e7],col=[0.0, 0.66, 0.42],text_col='w',fs=30,zorder=2,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/RedGiants.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def WhiteDwarfs(ax,text_label=r'{\bf White Dwarfs}',text_pos=[2e-24,4.2e7],col=[0.0, 0.66, 0.42],text_col='w',fs=30,zorder=2,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/WhiteDwarfs.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def HSi(ax,text_label=r'{\bf H/Si}',text_pos=[1e-20,2e-4],rotation=23,col='#730f3a',text_col='w',fs=20,zorder=-0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/HSi.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def AURIGA(ax,text_label=r'{\bf AURIGA}',text_pos=[0.8e-11,0.01e-2],rotation=-90,col='darkred',text_col='darkred',fs=17,zorder=0.01,text_on=True,Projection=False,edgealpha=1,lw=0):
        dat = loadtxt("limit_data/ScalarElectron/AURIGA.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def I2(ax,text_label=r'{\bf I}$_2$',text_pos=[0.33e-12,2.0e6],rotation=20,col='#b52452',text_col='w',fs=19,zorder=0.11,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/I2.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def GEO600(ax,text_label=r'{\bf GEO600}',text_pos=[4e-13,2e2],rotation=0,col='#b5260d',text_col='w',fs=20,zorder=0.109,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/GEO600.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def HQuartzSapphire(ax,text_label=r'\center{{\bf H/Quartz/Sapphire}}',text_pos=[0.8e-18,1e4],rotation=0,col='#a81313',text_col='w',fs=20,zorder=0.11,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/HQuartzSapphire.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def DAMNED(ax,text_label=r'{\bf DAMNED}',text_pos=[4.6e-11,1.55e4],rotation=90,col='#b5243f',text_col='w',fs=12,zorder=0.12,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/DAMNED.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def CsCav(ax,text_label=r'{\bf Cs/Cav}',text_pos=[2.9e-9,0.07e7],rotation=20,col='red',text_col='w',fs=16,zorder=0.11,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/CsCav.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def Holometer(ax,text_label=r'{\bf Holometer}',text_pos=[1.3e-9,3e4],rotation=0,col='#b53724',text_col='#b53724',fs=15,zorder=0.15,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/Holometer.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def RbQuartz(ax,text_label=r'{\bf Rb/Quartz}',text_pos=[2e-14,6e3],rotation=25,col='#c11a4e',text_col='w',fs=15,zorder=0.10999,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/RbQuartz.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def YbCs(ax,text_label=r'{\bf Yb/Cs}',text_pos=[1.8e-22,1.3e-5],rotation=0,col='#a11b33',text_col='w',fs=16,zorder=-1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/YbCs.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def LIGO(ax,text_label=r'{\bf LIGO}',text_pos=[0.53e-13,0.07e3],rotation=90,col='#c3151d',text_col='w',fs=15,zorder=0.101,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/LIGO.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    
    # Projections
    def AEDGE(ax,text_label=r'{\bf AEDGE}',text_pos=[1e-16,0.1e-11],rotation=51,col='#eb4034',text_col='#eb4034',fs=20,zorder=0,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/Projections/AEDGE.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def AION(ax,text_label=r'{\bf AION-km}',text_pos=[1e-14,0.1e-5],rotation=52,col='#eb4034',text_col='#eb4034',fs=20,zorder=0,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/Projections/AION-km.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def MAGIS(ax,text_label=r'{\bf MAGIS-km}',text_pos=[3e-16,0.2e-6],rotation=36,col='#eb4034',text_col='#eb4034',fs=20,zorder=0,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/Projections/MAGIS-km.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return    
   


        
    def DUAL(ax,text_label=r'{\bf DUAL}',text_pos=[3e-11,0.1e-4],rotation=0,col='#eb4034',text_col='#eb4034',fs=15,zorder=0,text_on=True,Projection=False,edgealpha=1,lw=1):
        dat = loadtxt("limit_data/ScalarElectron/Projections/DUAL.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
        
    def Resonators(ax,text_label=r'{\bf Resonators}',ms=7,alpha=0.75,text_pos=[0.1e-9,0.9e-4],rotation=23,rotation2=90,col='#690c43',text_col='#690c43',fs=25,fs2=13,zorder=0.2,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/Projections/Resonator-Sapphire.txt")
        plt.plot(dat[:-10000,0],dat[:-10000,1],'--',color=col,zorder=zorder,alpha=alpha,lw=lw)
        dat = loadtxt("limit_data/ScalarElectron/Projections/Resonator-Pillar.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=zorder,alpha=alpha,lw=lw)
        dat = loadtxt("limit_data/ScalarElectron/Projections/Resonator-Quartz.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=zorder,alpha=alpha,lw=lw)
        dat = loadtxt("limit_data/ScalarElectron/Projections/Resonator-Helium.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=zorder,alpha=alpha,lw=lw)

        ax.text(1.8e-11,2.5e-1,'Helium',rotation=rotation2,fontsize=fs2,color=text_col,alpha=alpha)
        ax.text(1.2e-10,1e-2,'Sapphire',rotation=rotation2,fontsize=fs2,color=text_col,alpha=alpha)
        ax.text(4e-9,0.5e-1,'Pillar',rotation=rotation2,fontsize=fs2,color=text_col,alpha=alpha)
        ax.text(4.5e-7,0.8e3,'Quartz BAW',rotation=rotation2,fontsize=fs2,color=text_col,alpha=alpha)
        plt.text(text_pos[0],text_pos[1],text_label,rotation=rotation,color=text_col,fontsize=fs,alpha=alpha)

        return
    
    def OpticalMW(ax,text_label=r'{\bf Optical-MW clock}',text_pos=[3e-22,7e-8],rotation=29,col='#703e41',text_col='#703e41',fs=20,zorder=0,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/Projections/OpticalMW.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def SrOH(ax,text_label=r'{\bf SrOH}',text_pos=[3e-22,20e-10],rotation=30,col='#703e41',text_col='#703e41',fs=20,zorder=0,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/Projections/SrOH.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def CavityCavity(ax,text_label=r'{\bf Cavity}',text_pos=[5e-13,2e-4],rotation=25,col='#703e41',text_col='#703e41',fs=13,zorder=0,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/ScalarElectron/Projections/CavityCavity.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,linestyle='--',edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def IPTA(ax,text_label=r'{\bf IPTA}',text_pos=[5e-24,2e-7],rotation=0,col='#274f70',text_col='#274f70',fs=20,zorder=-1,text_on=True,Projection=False,edgealpha=1,lw=2):
        dat = loadtxt("limit_data/ScalarElectron/IPTA.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

class VectorBL():
    def MICROSCOPE(ax,text_label=r'{\bf MICROSCOPE}',text_pos=[1.5e-22,2e-24],col='#84878c',text_col='k',fs=17,zorder=0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/VectorB-L/MICROSCOPE.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def EotWashEP(ax,text_label=r'{\bf E\"ot-Wash (EP)}',rotation=15,text_pos=[0.1e-8,0.5e-21],col='gray',text_col='k',fs=18,zorder=0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/VectorB-L/EotWashEP.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def InverseSquareLaw(ax,text_label=r'{\bf ISL}',rotation=60,text_pos=[9.9e-4,5.5e-19],col='darkgray',text_col='k',fs=18,zorder=0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/VectorB-L/InverseSquareLaw.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def Casimir(ax,text_label=r'{\bf Casimir}',rotation=60,text_pos=[3e-2,0.7e-14],col='silver',text_col='k',fs=18,zorder=0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/VectorB-L/Casimir.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
     
    def DMStability(ax,text_label=r'{\bf DM decays}',text_pos=[1e1,5e-16],rotation=-24,col='royalblue',text_col='w',fs=20,zorder=0.0,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/VectorB-L/DMStability.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def Sun(ax,text_label=r'{\bf Sun}',text_pos=[0.6e2,2e-14],rotation=-45,col='forestgreen',text_col='w',fs=20,zorder=0.2,text_on=True,Projection=False,edgealpha=1,lw=1.2):
        dat = loadtxt("limit_data/VectorB-L/Sun.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def HorizontalBranch(ax,text_label=r'{\bf HB}',text_pos=[6e2,1.5e-14],rotation=-45,col=[0.0, 0.66, 0.42],text_col='w',fs=20,zorder=0.19,text_on=True,Projection=False,edgealpha=1,lw=1.2):
        dat = loadtxt("limit_data/VectorB-L/HorizontalBranch.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def EotWashDM(ax,text_label=r'{\bf E\"ot-Wash (DM)}',text_pos=[0.08e-17,0.5e-23],rotation=90,col='darkred',text_col='w',fs=20,zorder=0.2,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/VectorB-L/EotWashDM.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
        
    def LIGO(ax,text_label='',text_pos=[1e-13,3e-20],rotation=90,col='crimson',text_col='w',fs=17,zorder=0.21,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/VectorB-L/LIGO-O1.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def LIGOVirgo(ax,text_label=r'{\bf LIGO/Virgo (DM)}',text_pos=[0.5e-12,2e-21],rotation=90,col='crimson',text_col='w',fs=20,zorder=0.2,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/VectorB-L/LIGOVirgo.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def LISAPathfinder(ax,text_label=r'{\bf LISA Pathfinder',text_pos=[3e-17,0.3e-15],rotation=70,col='#6b0a24',text_col='w',fs=17,zorder=0.21,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/VectorB-L/LISAPathfinder.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def PPTA(ax,text_label=r'{\bf PPTA}',text_pos=[2e-22,1e-21],rotation=90,col='#692820',text_col='w',fs=19,zorder=0.21,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/VectorB-L/PPTA.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def MAGIS(ax,text_label=r'{\bf MAGIS-100} (upgrade)',text_pos=[0.02e-20,0.75e-28],rotation=0,col='#a10649',text_col='#a10649',fs=16,zorder=0.0,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        #dat = loadtxt("limit_data/VectorB-L/Projections/MAGIS100-Initial.txt")
        #UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        dat = loadtxt("limit_data/VectorB-L/Projections/MAGIS100-Upgrade.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        
        #plt.text(0.04e-19,0.6e-26,'Initial',color=text_col,fontsize=fs*0.75,ha='center')
        #plt.text(0.04e-19,2.3e-28,'Upgrade',color=text_col,fontsize=fs*0.75,ha='center')
        return
    

    def STE_QUEST(ax,text_label=r'{\bf STE-QUEST}',text_pos=[1.5e-22,0.9e-26],rotation=0,col='#752b29',text_col='#752b29',fs=13,zorder=0.25,text_on=True,Projection=False,edgealpha=1,lw=2):
        dat = loadtxt("limit_data/VectorB-L/Projections/STE-QUEST.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def OptomechanicalMembranes(ax,text_label=r'{\bf \noindent Optomechanical \newline \indent membranes}',text_pos=[0.3e-11,0.4e-25],rotation=55,col='#961c06',text_col='#961c06',fs=15,zorder=0.25,text_on=True,Projection=False,edgealpha=1,lw=1.2):
        dat = loadtxt("limit_data/VectorB-L/Projections/OptomechanicalMembranes.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def LISA(ax,text_label=r'{\bf LISA}',text_pos=[1.3e-17,1.5e-27],rotation=0,col='darkred',text_col='darkred',fs=15,zorder=0.25,text_on=True,Projection=False,edgealpha=1,lw=2):
        dat = loadtxt("limit_data/VectorB-L/Projections/LISA.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def Asteroids(ax,text_label=r'{\bf Asteroids}',text_pos=[4.2e-20,0.35e-26],rotation=0,col='red',text_col='red',fs=14,zorder=0.25,text_on=True,Projection=False,edgealpha=1,lw=2):
        dat = loadtxt("limit_data/VectorB-L/Projections/Asteroids.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def SKA(ax,text_label=r'{\bf SKA}',text_pos=[3e-22,5e-26],rotation=60,col='green',text_col='green',fs=15,zorder=-1,text_on=True,Projection=False,edgealpha=1,lw=2):
        dat = loadtxt("limit_data/VectorB-L/Projections/SKA.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
    
    def TorsionBalance(ax,text_label=r'{\bf Torsion balance (future)}',text_pos=[1e-14,3e-29],rotation=63,col='gray',text_col='gray',fs=15,zorder=0.0,text_on=True,Projection=False,edgealpha=1,lw=2):
        dat = loadtxt("limit_data/VectorB-L/Projections/TorsionBalance.txt")
        UnfilledLimit(ax,dat,text_label,y2=1e20,rotation=rotation,text_pos=text_pos,text_col=text_col,edgecolor=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return
