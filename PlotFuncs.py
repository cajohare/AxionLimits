#================================PlotFuncs.py==================================#
# Created by Ciaran O'Hare 2020

# Description:
# This file has many functions which are used throughout the project, but are
# all focused around the bullshit that goes into making the plots

#==============================================================================#

from numpy import *
from numpy.random import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from matplotlib import colors
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
from scipy.stats import norm

pltdir = 'plots/'
pltdir_png = pltdir+'plots_png/'

#==============================================================================#
#==============================================================================#
class AxionPhoton():
    def FigSetup(xlab=r'$m_a$ [eV]',ylab='',\
                     g_min = 1.0e-19,g_max = 1.0e-6,\
                     m_min = 1.0e-12,m_max = 1.0e7,\
                     lw=2.5,lfs=45,tfs=25,tickdir='out',\
                     Grid=False,Shape='Rectangular',mathpazo=False,TopAndRightTicks=False):

            plt.rcParams['axes.linewidth'] = lw
            plt.rc('text', usetex=True)
            plt.rc('font', family='serif',size=tfs)

            if mathpazo:
                mpl.rcParams['text.latex.preamble'] = [r'\usepackage{mathpazo}']

            if Shape=='Wide':
                fig = plt.figure(figsize=(16.5,5))
            elif Shape=='Rectangular':
                fig = plt.figure(figsize=(16.5,11))

            ax = fig.add_subplot(111)

            ax.set_xlabel(xlab,fontsize=lfs)
            ax.set_ylabel(ylab,fontsize=lfs)

            ax.tick_params(which='major',direction=tickdir,width=2.5,length=13,right=TopAndRightTicks,top=TopAndRightTicks,pad=7)
            ax.tick_params(which='minor',direction=tickdir,width=1,length=10,right=TopAndRightTicks,top=TopAndRightTicks)


            ax.set_yscale('log')
            ax.set_xscale('log')
            ax.set_xlim([m_min,m_max])
            ax.set_ylim([g_min,g_max])

            locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=50)
            locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10)*.1,numticks=100)
            ax.xaxis.set_major_locator(locmaj)
            ax.xaxis.set_minor_locator(locmin)
            ax.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())

            locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100)
            locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10)*.1,numticks=100)
            ax.yaxis.set_major_locator(locmaj)
            ax.yaxis.set_minor_locator(locmin)
            ax.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())

            if Shape=='Rectangular':
                plt.xticks(rotation=20)

            if Grid:
                ax.grid(zorder=0)
            return fig,ax

    def QCDAxion(ax,coupling='Photon',
                      C_logwidth=10,KSVZ_on=True,DFSZ_on=True,
                      cmap='YlOrBr',fs=18,RescaleByMass=False):
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        ## QCD Axion band:
        g_min,g_max = ax.get_ylim()
        m_min,m_max = ax.get_xlim()

        # Mass-coupling relation
        def g_x(C_ag,m_a):
            return 2e-10*C_ag*m_a
        KSVZ = 1.92
        DFSZ = 0.75

        if rs1==0:
            # Plot Band
            n = 200
            g = logspace(log10(g_min),log10(g_max),n)
            m = logspace(log10(m_min),log10(m_max),n)
            QCD = zeros(shape=(n,n))
            for i in range(0,n):
                QCD[:,i] = norm.pdf(log10(g)-log10(g_x(1.0,m[i])),0.0,0.8)
            cols = cm.get_cmap(cmap)
            cols.set_under('w') # Set lowest color to white
            vmin = amax(QCD)/(C_logwidth/2)
            plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=0.9,zorder=0)
            plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=0.9,zorder=0)
            plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=0.9,zorder=0)

            # QCD Axion models
            rot = 45.0
            trans_angle = plt.gca().transData.transform_angles(array((rot,)),array([[0, 0]]))[0]
            m2 = array([1e-9,5e-8])
            if KSVZ_on:
                plt.plot(m,g_x(KSVZ,m),'-',linewidth=2,color=cols(1.0),zorder=0)
                plt.text(1e-8,g_x(KSVZ,1e-8)*1.05,r'{\bf KSVZ}',fontsize=fs,rotation=trans_angle,color=cols(1.0),ha='left',va='bottom',rotation_mode='anchor')
            if DFSZ_on:
                plt.plot(m,g_x(DFSZ,m),'-',linewidth=2,color=cols(1.0),zorder=0)
                plt.text(5e-8,g_x(DFSZ,5e-8)/1.5,r'{\bf DFSZ II}',fontsize=fs,rotation=trans_angle,color=cols(1.0),ha='left',va='top',rotation_mode='anchor')
        else:
            C_min,C_max = ax.get_ylim()
            n = 200
            C = logspace(log10(C_min),log10(C_max),n)
            m = logspace(log10(m_min),log10(m_max),n)
            QCD = zeros(shape=(n,n))
            for i in range(0,n):
                QCD[:,i] = norm.pdf(log10(C),0.0,0.8)
            cols = cm.get_cmap(cmap)
            cols.set_under('w') # Set lowest color to white
            vmin = amax(QCD)/(C_logwidth/2)
            plt.contourf(m, C, QCD, 50,cmap=cols,vmin=vmin,vmax=0.9,zorder=0)
            plt.contourf(m, C, QCD, 50,cmap=cols,vmin=vmin,vmax=0.9,zorder=0)
            plt.contourf(m, C, QCD, 50,cmap=cols,vmin=vmin,vmax=0.9,zorder=0)
            #plt.plot([1e-9,1e0],[1.92,1.92],'-',lw=2,color='k')
            plt.plot([1e-9,1e0],[0.75,0.75],'-',lw=2,color='k')
            #plt.text(2e-1,1.92*1.2,r'{\bf KSVZ}',fontsize=fs,color='k')
            plt.text(1e-2,0.75/3,r'{\bf DFSZ II}',fontsize=fs,color='k')
        return


    def ADMX(ax,col=[0.8, 0.0, 0.0],projection=False,fs=15,RescaleByMass=False):
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        # 2018: arXiv[1804.05750]
        # 2019: arXiv[1910.08638]
        y2 = ax.get_ylim()[1]
        col = [0.8, 0.0, 0.0]
        dat = loadtxt("limit_data/AxionPhoton/ADMX.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/AxionPhoton/ADMX2018.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/AxionPhoton/ADMX2019_1.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/AxionPhoton/ADMX2019_2.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)

        if projection:
            # ADMX arXiv[1804.05750]
            dat = loadtxt("limit_data/AxionPhoton/Projections/ADMX_Projected.txt")
            plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
            plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.1)
            if rs1==0:
                plt.text(4e-5,9e-16,r'{\bf ADMX}',fontsize=20,color=col,rotation=0,ha='left',va='top')
                plt.plot([4e-5,3e-5],[9e-16,2.1e-15],'k-',lw=1.5)
            else:
                plt.text(0.9e-6,0.15,r'{\bf ADMX}',fontsize=fs,color=col,rotation=0,ha='left',va='top')
        else:
            if rs1==0:
                plt.text(0.7e-6,1e-13,r'{\bf ADMX}',fontsize=fs,color=col,rotation=90,ha='left',va='top')

        return


    def NeutronStars(ax,col=[0.1, 0.5, 0.2],fs=15,RescaleByMass=False):
        # Neutron stars arXiv:[2004.00011]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt('limit_data/AxionPhoton/NeutronStars.txt')
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        if rs1==0:
            plt.text(5e-6,1e-12,r'{\bf Neutron stars}',fontsize=fs,color='w',ha='left')
        else:
            plt.text(1e-7,4e3,r'{\bf Neutron}',fontsize=fs,color=col,ha='center')
            plt.text(1e-7,1e3,r'{\bf stars}',fontsize=fs,color=col,ha='center')
            plt.plot([3.5e-7,7e-6],[6e3,2e4],lw=1.5,color=col)

    def RBF_UF(ax,col ='darkred',fs=13,RescaleByMass=False):
        # UF: Phys. Rev. D42, 1297 (1990).
        # RBF: Phys. Rev. Lett. 59, 839 (1987).
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/RBF_UF_Haloscopes.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        if rs1==0:
            plt.text(0.4e-5,3e-11,r'{\bf RBF+UF}',fontsize=fs,color='w',rotation=-90,ha='left',va='top')
        else:
            plt.text(0.7e-5,4e3,r'{\bf RBF}',fontsize=fs,color='w',rotation=0,ha='center',va='top')
            plt.text(0.7e-5,1e3,r'{\bf UF}',fontsize=fs,color='w',rotation=0,ha='center',va='top')

        return

    def HAYSTAC(ax,col=[0.88, 0.07, 0.37],fs=13,RescaleByMass=False,projection=True):
        # HAYSTAC arXiv:[1803.03690]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = 3
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = 0
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/HAYSTAC.txt")
        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=3)
            if projection:
                plt.text(2.4e-5,4e-12,r'{\bf HAYSTAC}',fontsize=fs,color=col,rotation=-90,ha='left',va='top')
            else:
                plt.text(2.4e-5,5e-13,r'{\bf HAYSTAC}',fontsize=fs,color=col,rotation=-90,ha='left',va='top')
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',zorder=zo,lw=4)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=3)
            plt.text(dat[0,0],y2*1.2,r'{\bf HAYSTAC}',fontsize=fs,color=col,rotation=40,ha='left',rotation_mode='anchor')
            plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)
        return

    def CAPP(ax,col=[1, 0.1, 0.37],fs=15,RescaleByMass=False):
        # CAPP arXiv:[2001.05102]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = 3
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = 0
        dat = loadtxt("limit_data/AxionPhoton/CAPP-8TB.txt")
        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=3)
            plt.text(1e-5,1e-13,r'{\bf CAPP}',fontsize=fs,color=col,rotation=-90,ha='center',va='top')
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',zorder=zo,lw=4)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=3)
            plt.text(dat[0,0],y2*1.8,r'{\bf CAPP}',fontsize=fs,color=col,rotation=40,ha='left',va='top',rotation_mode='anchor')
            plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)
        return

    def QUAX(ax,col='crimson',fs=15,RescaleByMass=False):
        # QUAX arXiv:[1903.06547]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = 3
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = 0
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/QUAX.txt")

        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=2,zorder=zo)
            plt.text(5.2e-5,4e-11,r'{\bf QUAX}',fontsize=fs,color=col,rotation=-90,ha='center',va='top')
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',lw=4,zorder=zo)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=3,zorder=zo)
            plt.text(dat[0,0]*1.3,y2*1.2,r'{\bf QUAX}',fontsize=fs,color=col,rotation=40,ha='left',rotation_mode='anchor')
            plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)
        return

    def ABRACADABRA(ax,col=[0.83, 0.07, 0.37],fs=15,projection=False,RescaleByMass=False):
        # ABRACADABRA arXiv:[1810.12257]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/ABRACADABRA.txt")
        n = shape(dat)[0]
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=2)
        x = dat[arange(0,n,20),0]
        y = dat[arange(0,n,20),1]
        y[-1] = y2
        plt.plot(x,y/(rs1*2e-10*x+rs2),'k-',lw=1,zorder=10,alpha=0.5)
        if rs1==0:
            plt.text(1.5e-9,3e-8,r'{\bf ABRA}',fontsize=fs,color='w',rotation=0,ha='center',va='top',zorder=10)
            plt.text(1.5e-9,1e-8,r'10 cm',fontsize=fs,color='w',rotation=0,ha='center',va='top',zorder=10)

        if projection:
            dat = loadtxt("limit_data/AxionPhoton/Projections/ABRACADABRA.txt")
            plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
            plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.1)
            if rs1==0:
                plt.text(1e-12,2.5e-18,r'{\bf ABRACADABRA}',fontsize=fs-1,color=col,rotation=13,ha='left',va='top')
            else:
                plt.text(1.3e-9,1.0e2,r'{\bf ABRACADABRA}',fontsize=fs-1,color=col,rotation=0,ha='left',va='top')
                plt.plot([dat[-1,0],dat[-1,0]],[dat[-1,1]/(rs1*2e-10*dat[-1,0]+rs2),1e6],lw=1.5,color=col,zorder=0)
        return

    def ORGAN(ax,col='crimson',projection=False,fs=15,RescaleByMass=False):
        # ORGAN arXiv[1706.00209]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        col = [0.8, 0.0, 0.0]
        dat = loadtxt("limit_data/AxionPhoton/ORGAN.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=col,facecolor=col,zorder=0.1,lw=2)

        if projection:
            dat = loadtxt("limit_data/AxionPhoton/Projections/ORGAN_Projected.txt")
            plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
            plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.1)
            if rs1==0:
                plt.text(5e-4,1.15e-14,r'{\bf ORGAN}',fontsize=18,color=col,rotation=0,ha='left',va='top')
                plt.plot([5e-4,1.5e-4],[1.3e-14,6e-13],'k-',lw=1.5)
            else:
                plt.text(1.2e-4,1e3,r'{\bf ORGAN}',fontsize=18,color=col,rotation=-90,ha='left',va='top')

        else:
            if rs1==0:
                plt.text(110e-6,6e-11,r'{\bf ORGAN}',fontsize=fs,color=col,rotation=-90,ha='left',va='top')
        return


    def MADMAX(ax,col=[0.6, 0.1, 0.1],fs=18,RescaleByMass=False):
        # MADMAX arXiv[2003.10894]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/MADMAX.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.2)
        if rs1==0:
            plt.text(1.5e-4,3.5e-15,r'{\bf MADMAX}',fontsize=18,color=col,rotation=0,ha='left',va='top')
            plt.plot([3e-4,1.3e-4],[4.5e-15,2.6e-14],'k-',lw=1.5)
        else:
            plt.text(4e-5,3.5e-1,r'{\bf MADMAX}',fontsize=fs,color=col,rotation=0,ha='left',va='top')
        return

    def KLASH(ax,col=[0.8, 0.1, 0.2],fs=15,RescaleByMass=False):
        # KLASH arXiv:[1707.06010]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/KLASH.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,facecolor=col,zorder=0,alpha=0.1)
        if rs1==0:
            plt.text(1e-7,1e-12,r'{\bf KLASH}',rotation=90,fontsize=fs,color=col,ha='left',va='top')
        else:
            plt.text(2.5e-7,3e2,r'{\bf KLASH}',rotation=90,fontsize=fs,color=col,ha='left',va='top')

    def BRASS(ax,col=[0.5, 0.1, 0.2],fs=15,RescaleByMass=False):
        # BRASS http://www.iexp.uni-hamburg.de/groups/astroparticle/brass/brassweb.htm
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/BRASS.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,facecolor=col,zorder=0,alpha=0.1)
        if rs1==0:
            plt.text(2.3e-3,0.6e-10,r'{\bf BRASS}',rotation=56,fontsize=fs,color=col,ha='left',va='top')
        else:
            plt.text(1e-3,0.12e3,r'{\bf BRASS}',rotation=15,fontsize=fs,color=col,ha='left',va='top')


    def TOORAD(ax,col=[0.8, 0.1, 0.2],fs=15,RescaleByMass=False):
        # TOORAD arXiv[1807.08810]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/TOORAD.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,facecolor=col,zorder=0,alpha=0.1)
        if rs1==0:
            plt.text(0.5e-2,5e-14,r'{\bf TOORAD}',rotation=0,fontsize=18,color=col,ha='left',va='top')
            plt.plot([0.5e-2,0.21e-2],[5e-14,1e-13],'k-',lw=1.5)
        else:
            plt.text(0.6e-3,4e-1,r'{\bf TOORAD}',rotation=-25,fontsize=fs,color=col,ha='left',va='top')

    def LAMPOST(ax,col=[0.8, 0.1, 0.2],fs=15,RescaleByMass=False):
        # LAMPOST arXiv[1803.11455]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/LAMPOST.txt",delimiter=',')
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,facecolor=col,zorder=0,alpha=0.1)

        if rs1==0:
            plt.text(0.8e-1,5e-12,r'{\bf LAMPOST}',rotation=-90,fontsize=fs,color=col,ha='left',va='top')
        else:
            plt.text(0.9e-1,1.9e-1,r'{\bf LAMPOST}',rotation=0,fontsize=fs,color=col,ha='left',va='top')


    # Low mass ALP haloscopes
    def DANCE(ax,col=[0.8, 0.1, 0.2],fs=15):
        # DANCE arXiv[1911.05196]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/Projections/DANCE.txt")
        plt.plot(dat[:,0],dat[:,1],'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0,alpha=0.1)
        plt.text(1.7e-12,2e-13,r'{\bf DANCE}',rotation=50,fontsize=fs,color=col,ha='left',va='top')

    def aLIGO(ax,col=[0.8, 0.1, 0.2],fs=15):
        # aLIGO arXiv[1903.02017]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/Projections/aLIGO.txt")
        plt.plot(dat[:,0],dat[:,1],'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0,alpha=0.1)
        plt.text(0.2e-9,0.35e-13,r'{\bf aLIGO}',rotation=0,fontsize=fs,color=col,ha='left',va='top')

    def ADBC(ax,col=[0.8, 0.1, 0.2],fs=15):
        # ADBC arXiv[1809.01656]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/Projections/ADBC.txt")
        plt.plot(dat[:,0],dat[:,1],'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0,alpha=0.1)
        plt.text(1e-11,1.3e-12,r'{\bf ADBC}',rotation=26,fontsize=fs,color=col,ha='left',va='top')

    def SHAFT(ax,col='red',fs=16):
        # SHAFT arXiv:[2003.03348]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/SHAFT.txt")
        n = shape(dat)[0]
        x = dat[arange(0,n,2),0]
        y = dat[arange(0,n,2),1]
        y[-1] = y2
        plt.plot(x,y,'k-',lw=1,zorder=10,alpha=0.5)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.8)
        plt.text(0.8e-10,3e-10,r'{\bf SHAFT}',fontsize=fs,color='w',rotation=0,ha='center',va='top',zorder=9)
        return

    def ALPS(ax,col=[0.8, 0.25, 0.33],fs=15):
        # ALPS-I arXiv:[1004.1313]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/ALPS.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',lw=2.5,zorder=1.53,alpha=0.5)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.53,lw=0.01)
        plt.text(1e-5,7e-8,r'{\bf ALPS-I}',fontsize=20,color='w')

    def OSQAR(ax,col=[0.6, 0.2, 0.25],fs=15):
        # OSQAR arXiv:[]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/OSQAR.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',lw=2.5,zorder=1.52,alpha=0.5)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.52,lw=0.01)
        plt.text(1e-5,1.5e-8,r'{\bf OSQAR}',fontsize=17,color='w')

    def PVLAS(ax,col=[0.4, 0.2, 0.2],fs=15):
        # PVLAS arXiv:[]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/PVLAS.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',lw=2.5,zorder=1.51,alpha=0.4)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.51,lw=0.01)
        plt.text(2e-3,9e-8,r'{\bf PVLAS}',fontsize=17,color='w',rotation=45)


    def CROWS(ax,col=[0.7, 0.2, 0.2],fs=15):
        # CROWS arXiv:[1310.8098]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/CROWS.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',lw=2.5,zorder=1.54,alpha=0.4)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.54,lw=0.01)
        plt.text(1e-7,1.5e-7,r'{\bf CROWS}',fontsize=17,color='w',rotation=0)


    ####################################################
    def Helioscopes(ax,col=[0.5, 0.0, 0.13],fs=25,projection=True,RescaleByMass=False):
        # CAST arXiv:[1705.02290]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/CAST_highm.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',lw=2,zorder=1.49,alpha=0.5)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor='k',facecolor=col,zorder=1.49,lw=0.1)
        dat = loadtxt("limit_data/AxionPhoton/CAST.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',lw=2,zorder=1.5,alpha=0.5)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor='k',facecolor=col,zorder=1.5,lw=0.1)
        if rs1==0:
            plt.text(1e-3,5e-10,r'{\bf CAST}',fontsize=fs+4,color='w',rotation=0,ha='center',va='top')
        else:
            plt.text(4e-2,5e3,r'{\bf CAST}',fontsize=fs+4,color='w',rotation=0,ha='center',va='top')

        if projection:
            # IAXO arXiv[1212.4633]
            IAXO_col = 'purple'
            IAXO = loadtxt("limit_data/AxionPhoton/Projections/IAXO.txt")
            plt.plot(IAXO[:,0],IAXO[:,1]/(rs1*2e-10*IAXO[:,0]+rs2),'--',linewidth=2.5,color=IAXO_col,zorder=0.5)
            plt.fill_between(IAXO[:,0],IAXO[:,1]/(rs1*2e-10*IAXO[:,0]+rs2),y2=y2,edgecolor=None,facecolor=IAXO_col,zorder=0,alpha=0.3)
            if rs1==0:
                plt.text(0.35e-1,0.2e-11,r'{\bf IAXO}',fontsize=fs,color=IAXO_col,rotation=45)
            else:
                plt.text(0.7e-2,0.15e1,r'{\bf IAXO}',fontsize=fs,color=IAXO_col,rotation=-20)
        return


    def Haloscopes(ax,projection=True,fs=20):
        AxionPhoton.ADMX(ax,projection=projection,fs=fs)
        AxionPhoton.RBF_UF(ax,fs=fs-2)
        AxionPhoton.HAYSTAC(ax,projection=projection)
        AxionPhoton.ABRACADABRA(ax,fs=fs,projection=projection)
        AxionPhoton.SHAFT(ax)
        AxionPhoton.CAPP(ax,fs=fs-4)
        AxionPhoton.ORGAN(ax,projection=projection)

        if projection:
            AxionPhoton.MADMAX(ax)
            AxionPhoton.KLASH(ax)
            AxionPhoton.TOORAD(ax)
            AxionPhoton.BRASS(ax)
            AxionPhoton.ADBC(ax)
            AxionPhoton.DANCE(ax)
            AxionPhoton.aLIGO(ax)
        else:
            AxionPhoton.QUAX(ax)
        return

    def LSW(ax,projection=True):
        AxionPhoton.PVLAS(ax)
        AxionPhoton.ALPS(ax)
        AxionPhoton.OSQAR(ax)
        AxionPhoton.CROWS(ax)
        return


    def AstroBounds(ax,projection=True,fs=15):
        y2 = ax.get_ylim()[1]
        ### Astrophysical constraints

        # SN-gamma rays arXiv:[1410.3747]
        SNgamma_col = [0.05, 0.5, 0.06]
        SNgamma = loadtxt("limit_data/AxionPhoton/SN-gamma.txt")
        plt.plot(SNgamma[:,0],SNgamma[:,1],'k-',alpha=0.6,zorder=0.21,lw=2)
        plt.fill_between(SNgamma[:,0],SNgamma[:,1],y2=y2,edgecolor=None,facecolor=SNgamma_col,zorder=0.21)
        plt.text(3e-11,2e-11,r'{\bf SN}-$\gamma$',fontsize=fs,color='w',ha='left',va='top')

        # M87 Limits from arXiv:[1703.07354]
        M87_col = [0.0, 0.66, 0.42]
        M87 = loadtxt("limit_data/AxionPhoton/M87.txt")
        plt.plot(M87[:,0],M87[:,1],'k-',lw=2,alpha=0.8,zorder=0.2)
        plt.fill_between(M87[:,0],M87[:,1],y2=y2,edgecolor=None,facecolor=M87_col,zorder=0.2)
        plt.text(1.4e-12,4e-12,r'\quad {\bf M87}',fontsize=fs,color='w',ha='left',va='top')

        # HYDRA-A arXiv:[1304.0989]
        HYDRA_col = [0.24, 0.71, 0.54]
        HYDRA = loadtxt("limit_data/AxionPhoton/HYDRA_A.txt")
        plt.plot(HYDRA[:,0],HYDRA[:,1],'k-',alpha=0.6,zorder=0.23,lw=2)
        plt.fill_between(HYDRA[:,0],HYDRA[:,1],y2=y2,edgecolor=None,facecolor=HYDRA_col,zorder=0.23)
        plt.text(1.5e-12,4e-11,r'{\bf Hydra}',fontsize=fs-2,color='w',ha='left',va='top')
        plt.text(3e-12,2e-11,r'\quad {\bf A}',fontsize=fs-2,color='w',ha='left',va='top')

        # HESS arXiv:[1304.0700]
        HESS_col = [0.0, 0.62, 0.38]
        HESS = loadtxt("limit_data/AxionPhoton/HESS.txt")
        plt.plot(HESS[:,0],HESS[:,1],'k-',alpha=0.6,zorder=0.2,lw=2)
        plt.fill_between(HESS[:,0],HESS[:,1],y2=y2,edgecolor=None,facecolor=HESS_col,zorder=0.2)
        plt.text(2e-8,1.6e-11,r'{\bf HESS}',fontsize=fs+1,color='k',ha='left',va='top')

        # Fermi NGC1275 arXiv:[1603.06978]
        Fermi_col = [0.0, 0.42, 0.24]
        Fermi1 = loadtxt("limit_data/AxionPhoton/Fermi1.txt")
        Fermi2 = loadtxt("limit_data/AxionPhoton/Fermi2.txt")
        plt.fill_between(Fermi1[:,0],Fermi1[:,1],y2=y2,edgecolor=Fermi_col,facecolor=Fermi_col,zorder=0.24,lw=3)
        plt.fill(Fermi2[:,0],1.01*Fermi2[:,1],edgecolor=Fermi_col,facecolor=Fermi_col,lw=3,zorder=0.24)
        Fermi1 = loadtxt("limit_data/AxionPhoton/Fermi_bound.txt")
        Fermi2 = loadtxt("limit_data/AxionPhoton/Fermi_hole.txt")
        plt.plot(Fermi1[:,0],Fermi1[:,1],'k-',alpha=0.5,lw=1.5,zorder=0.24)
        plt.plot(Fermi2[:,0],Fermi2[:,1],'k-',alpha=0.5,lw=1.5,zorder=0.24)
        plt.text(4.8e-10,1.2e-11,r'{\bf Fermi}',fontsize=fs,color='w',ha='left',va='top')

        # Optical telescope [astro-ph/0611502]
        Telescopes_col = [0.09, 0.45, 0.27]
        Telescopes = loadtxt("limit_data/AxionPhoton/Telescopes.txt")
        plt.fill_between(Telescopes[:,0],Telescopes[:,1],y2=y2,edgecolor=None,facecolor=Telescopes_col,zorder=0.2)
        plt.text(3.3,4e-12,r'{\bf Telescopes}',fontsize=fs,color=Telescopes_col,rotation=-90,ha='left',va='top')

        # Chandra arXiv:[1907.05475]
        Chandra_col = [0.0, 0.3, 0.24]
        Chandra = loadtxt('limit_data/AxionPhoton/Chandra.txt')
        plt.plot(Chandra[:,0],Chandra[:,1],'k-',alpha=0.8,lw=2,zorder=0.1)
        plt.fill_between(Chandra[:,0],Chandra[:,1],y2=y2,edgecolor=None,facecolor=Chandra_col,zorder=0.1)
        if projection==False:
            plt.text(1.1e-11,2e-12,r'{\bf Chandra}',fontsize=fs,color=Chandra_col,rotation=0,ha='left',va='top')

        if projection==True:
            # Fermi nearby SN prospects arXiv:[1609.02350]
            FermiSN = loadtxt("limit_data/AxionPhoton/Projections/FermiSN.txt")
            plt.fill_between(FermiSN[:,0],FermiSN[:,1],y2=y2,edgecolor=Fermi_col,linewidth=1.5,facecolor=Fermi_col,zorder=0.1,alpha=0.2)
            plt.text(1e-9,4e-12,r'{\bf Fermi SN}',fontsize=fs,color=Fermi_col,rotation=43,ha='left',va='top')


        return

    def Cosmology(ax,fs=30):
        y2 = ax.get_ylim()[1]
        ## Cosmology constraints see arXiv:[1210.3196] for summary
        # Xray Background
        XRAY_col = [0.03, 0.57, 0.82]
        XRAY = loadtxt("limit_data/AxionPhoton/XRAY.txt")
        plt.plot(XRAY[:,0],XRAY[:,1],color='k',alpha=0.5,zorder=0.3,lw=2)
        plt.fill_between(XRAY[:,0],XRAY[:,1],y2=1e-11,edgecolor=None,facecolor=XRAY_col,zorder=0.3)

        # Extragalactic background light
        EBL_col =  [0.0, 0.2, 0.6]
        EBL = loadtxt("limit_data/AxionPhoton/EBL.txt")
        EBL2 = loadtxt("limit_data/AxionPhoton/EBL2.txt")
        plt.plot(EBL[:,0],EBL[:,1],'k',lw=2.5,zorder=0.4,alpha=0.8)
        plt.fill_between(EBL[:,0],EBL[:,1],y2=y2,edgecolor=None,facecolor=EBL_col,zorder=0.5)
        plt.fill_between(EBL2[:,0],EBL2[:,1],y2=y2,edgecolor=None,facecolor=EBL_col,zorder=0.5)

        # Ionisation fraction
        x_ion_col = [0.27, 0.51, 0.71]
        x_ion = loadtxt("limit_data/AxionPhoton/x_ion.txt")
        plt.plot(x_ion[:,0],x_ion[:,1],'k',lw=2.5,zorder=0.4,alpha=0.8)
        plt.fill_between(x_ion[:,0],x_ion[:,1],y2=y2,edgecolor=None,facecolor=x_ion_col,zorder=0.5)

        # BBN+N_eff arXiv:[2002.08370]
        BBN_col = [0.27, 0.51, 0.71]
        BBN = loadtxt("limit_data/AxionPhoton/BBN_Neff.txt")
        plt.plot(BBN[:,0],BBN[:,1],'k',lw=2,zorder=0.4,alpha=0.5)
        plt.fill_between(BBN[:,0],BBN[:,1],y2=y2,edgecolor=None,facecolor=BBN_col,zorder=0.4)

        plt.text(3e3,0.8e-16,r'{\bf X-rays}',fontsize=fs,color='w',rotation=-50,ha='left',va='top')
        plt.text(1e4,5e-14,r'{\bf EBL}',fontsize=fs+5,color='w',rotation=-55,ha='left',va='top')
        plt.text(100.5744,5.1720e-11,r'{\bf Ionisation}',fontsize=fs-6,color='w',rotation=-90,ha='left',va='top')
        plt.text(40,4.1720e-11,r'{\bf fraction}',fontsize=fs-6,color='w',rotation=-90,ha='left',va='top')
        plt.text(0.05e6,8e-10,r'{\bf BBN}+$N_{\rm eff}$',fontsize=fs,color='w',rotation=-55,ha='left',va='top')


    def StellarBounds(ax,fs=30):
        y2 = ax.get_ylim()[1]
        # Stellar physics constraints

        # Globular clusters arXiv:[1406.6053]
        HB_col = [0.0, 0.66, 0.42]
        HB = loadtxt("limit_data/AxionPhoton/HorizontalBranch.txt")
        plt.plot(HB[:,0],HB[:,1],color='k',alpha=0.5,zorder=1,lw=2)
        plt.fill_between(HB[:,0],HB[:,1],y2=y2,edgecolor=None,facecolor=HB_col,zorder=1)

        # Solar neutrino B8 bound arXiv:[1501.01639]
        SolarNu_col = [0.01, 0.75, 0.24]
        SolarNu = loadtxt("limit_data/AxionPhoton/SolarNu.txt")
        plt.plot(SolarNu[:,0],SolarNu[:,1],color='k',lw=2,alpha=0.5,zorder=1)
        plt.fill_between(SolarNu[:,0],SolarNu[:,1],y2=y2,edgecolor=None,facecolor=SolarNu_col,zorder=1)

        # SN1987A-neutrinos updated arXiv:[1808.10136]
        SN = loadtxt("limit_data/AxionPhoton/SN1987A_2019.txt")
        plt.fill_between(SN[:,0],SN[:,1],y2=y2,edgecolor=None,facecolor='ForestGreen',zorder=0.1)
        # SN1987A-decay arXiv:[1702.02964]
        SN = loadtxt("limit_data/AxionPhoton/SN1987A_decay.txt")
        plt.fill_between(SN[:,0],SN[:,1],y2=y2,edgecolor=None,facecolor='ForestGreen',zorder=0.1)

        plt.text(0.4e6,6e-7,r'{\bf SN1987A}',fontsize=fs-9,color='w',rotation=-60,ha='left',va='top')
        plt.text(1e1,3e-9,r'{\bf Solar} $\nu$',fontsize=fs+3,color='w')
        plt.text(1.4e0,1.5e-10,r'{\bf Horizontal branch}',fontsize=fs-7,color='w')

#==============================================================================#
#==============================================================================#


#==============================================================================#
#==============================================================================#
class AxionElectron():
    def FigSetup(xlab=r'$m_a$ [eV]',ylab='$|g_{ae}|$',\
                     g_min = 1.0e-15,g_max = 1.0e-10,\
                     m_min = 1.0e-9,m_max = 1.0e4,\
                     lw=2.5,lfs=45,tfs=25,tickdir='out',\
                     Grid=False,Shape='Rectangular',mathpazo=False,
                     TopAndRightTicks=False):

            plt.rcParams['axes.linewidth'] = lw
            plt.rc('text', usetex=True)
            plt.rc('font', family='serif',size=tfs)

            if mathpazo:
                mpl.rcParams['text.latex.preamble'] = [r'\usepackage{mathpazo}']

            if Shape=='Wide':
                fig = plt.figure(figsize=(16.5,5))
            elif Shape=='Rectangular':
                fig = plt.figure(figsize=(16.5,11))

            ax = fig.add_subplot(111)

            ax.set_xlabel(xlab,fontsize=lfs)
            ax.set_ylabel(ylab,fontsize=lfs)

            ax.tick_params(which='major',direction=tickdir,width=2.5,length=13,right=TopAndRightTicks,top=TopAndRightTicks,pad=7)
            ax.tick_params(which='minor',direction=tickdir,width=1,length=10,right=TopAndRightTicks,top=TopAndRightTicks)


            ax.set_yscale('log')
            ax.set_xscale('log')
            ax.set_xlim([m_min,m_max])
            ax.set_ylim([g_min,g_max])

            locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=50)
            locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10)*.1,numticks=100)
            ax.xaxis.set_major_locator(locmaj)
            ax.xaxis.set_minor_locator(locmin)
            ax.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())

            locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100)
            locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10)*.1,numticks=100)
            ax.yaxis.set_major_locator(locmaj)
            ax.yaxis.set_minor_locator(locmin)
            ax.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())

            if Grid:
                ax.grid(zorder=0)
            return fig,ax

    def QCDAxion(ax,coupling='Photon',
                      C_logwidth=10,KSVZ_on=True,DFSZ_on=True,Hadronic_on=True,
                      cmap='YlOrBr',fs=25):
        ## QCD Axion band:
        g_min,g_max = ax.get_ylim()
        m_min,m_max = ax.get_xlim()

        # Mass-coupling relation
        def g_x(C_ae,m_a):
            return 8.943e-11*C_ae*m_a
        DFSZ_u = 1.0/3.0
        DFSZ_l = 2.0e-5
        KSVZ = 2e-4
        Had_u = 5e-3
        Had_l = 1.5e-4

        # QCD Axion models
        n = 200
        m = logspace(log10(m_min),log10(m_max),n)
        rot = 45.0
        trans_angle = plt.gca().transData.transform_angles(array((rot,)),array([[0, 0]]))[0]
        if DFSZ_on:
            col = 'goldenrod'
            plt.fill_between(m,g_x(DFSZ_l,m),y2=g_x(DFSZ_u,m),facecolor=col,zorder=0,alpha=0.5)
            plt.plot(m,g_x(DFSZ_l,m),'k-',lw=3.5,zorder=0)
            plt.plot(m,g_x(DFSZ_u,m),'k-',lw=3.5,zorder=0)
            plt.plot(m,g_x(DFSZ_l,m),'-',lw=2,zorder=0,color=col)
            plt.plot(m,g_x(DFSZ_u,m),'-',lw=2,zorder=0,color=col)
            plt.text(1e-4,g_x(DFSZ_u,1e-4)/1.5,r'{\bf DFSZ models}',fontsize=fs,rotation=trans_angle,color='k',ha='left',va='top',rotation_mode='anchor')
        if KSVZ_on:
            col = 'brown'
            plt.plot(m,g_x(KSVZ,m),'k-',lw=3.5,zorder=0.02)
            plt.plot(m,g_x(KSVZ,m),'-',lw=2,zorder=0.02,color=col)
            plt.text(0.8e-1,g_x(KSVZ,0.8e-1)*2.3,r'{\bf KSVZ}',fontsize=fs,rotation=trans_angle,color=col,ha='left',va='top',rotation_mode='anchor')
        if Hadronic_on:
            col = 'gold'
            plt.fill_between(m,g_x(Had_l,m),y2=g_x(Had_u,m),facecolor=col,zorder=0.01,alpha=0.6)
            plt.plot(m,g_x(Had_l,m),'k-',lw=3.5,zorder=0.01)
            plt.plot(m,g_x(Had_u,m),'k-',lw=3.5,zorder=0.01)
            plt.plot(m,g_x(Had_l,m),'-',lw=2,zorder=0.01,color=col)
            plt.plot(m,g_x(Had_u,m),'-',lw=2,zorder=0.01,color=col)
            plt.text(5e-3,g_x(Had_u,5e-3)/1.5,r'{\bf Hadronic models}',fontsize=fs-5,rotation=trans_angle,color='k',ha='left',va='top',rotation_mode='anchor')

        return

    def XENON1T(ax,col='m',fs=20):
        # XENON1T LDM Searches arXiv:[1907.11485]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/XENON1T.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=0.6,zorder=0.51,lw=2)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.51)
        plt.text(0.25e2,4e-14,r'{\bf XENON1T}',fontsize=fs,color=col,ha='left',va='top')
        return

    def LUX(ax,col='darkorchid',fs=20):
        # LUX arXiv:[1704.02297]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/LUX.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=0.6,zorder=0.52,lw=2)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.52)
        plt.text(0.5e-8,6e-12,r'{\bf LUX}',fontsize=30,color='w',alpha=0.8,ha='left',va='top')
        return

    def PandaX(ax,col='mediumvioletred',fs=20):
        # PandaX arXiv:[1707.07921]
        y2 = ax.get_ylim()[1]
#         Currently not using Solar pandaX limit
#         dat = loadtxt("limit_data/AxionElectron/PandaX_Solar.txt")
#         plt.plot(dat[:,0],dat[:,1],'k-',alpha=0.6,zorder=0.53,lw=2)
#         plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.53)
        dat = loadtxt("limit_data/AxionElectron/PandaX.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=0.6,zorder=0.53,lw=2)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.53)
        plt.text(1.2e3,4.5e-13,r'{\bf PandaX}',fontsize=fs-2,color='w',ha='left',va='top',rotation=20)
        return

    def EDELWEISS(ax,col='crimson',projection=True,fs=20):
        # EDELWEISS arXiv:[1808.02340]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/EDELWEISS.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=0.6,zorder=0.57,lw=2)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.57)
        if projection:
            dat = loadtxt("limit_data/AxionElectron/Projections/EDELWEISS.txt")
            plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=0.56,lw=3)
        plt.text(9e0,7e-13,r'{\bf EDELWEISS}',fontsize=fs,color=col,ha='left',va='top')
        return

    def SuperCDMS(ax,col='orchid',fs=20):
        # SuperCDMS arXiv:[1911.11905]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/SuperCDMS.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.58)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=0.5,zorder=0.58,lw=3)
        plt.text(1e2,9e-12,r'{\bf SuperCDMS}',fontsize=fs,color='k',ha='left',va='top',alpha=0.8)
        return

    def DARWIN(ax,col='blueviolet',fs=20):
        # PandaX arXiv:[1606.07001]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/Projections/DARWIN.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=0.1,lw=3)
        plt.text(0.5e3,2e-14,r'{\bf DARWIN}',fontsize=fs,color=col,ha='left',va='top')
        return

    def Semiconductors(ax,col='purple',fs=20):
        # ALP Absorption with semiconductors arXiv:[1608.02123]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/Projections/SemiconductorAbsorption.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=0.5,lw=3)
        plt.text(1e0,2.5e-12,r'{\bf Semiconductors}',fontsize=fs,color=col,ha='left',va='top',rotation=-80)
        return

    def UndergroundDetectors(ax,projection=True,fs=20):
        AxionElectron.LUX(ax,fs=fs)
        AxionElectron.PandaX(ax,fs=fs)
        AxionElectron.XENON1T(ax,fs=fs)
        AxionElectron.SuperCDMS(ax,fs=fs)
        AxionElectron.EDELWEISS(ax,fs=fs-5,projection=projection)
        if projection:
            AxionElectron.DARWIN(ax,fs=fs)
            AxionElectron.Semiconductors(ax,fs=fs-5)
        return

    def ElectronSpinMagnetometers(ax,col = 'darkred',fs=20):
        # Lawson et al. Reference: arXiv:[in preparation]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/Projections/ElectronSpinMagnetometers.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=0,lw=3)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.5)
        plt.text(1.4e-9,1e-13,r'{\bf Electron spin}',fontsize=fs,color=col,ha='left',va='top')
        plt.text(1.2e-9,0.7e-13,r'{\bf magnetometers}',fontsize=fs,color=col,ha='left',va='top')
        return

    def Haloscopes(ax,projection=True,fs=20):
        if projection:
            AxionElectron.ElectronSpinMagnetometers(ax)
        return

    def StellarBounds(ax,fs=30,Hint=True):
        y2 = ax.get_ylim()[1]
        # Stellar physics constraints
        # Red Giants arXiv:[1708.02111]
        RG_col = [0.0, 0.66, 0.42]
        dat = loadtxt("limit_data/AxionElectron/RedGiants.txt")
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=0.5,zorder=0.5,lw=2)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=RG_col,zorder=0.5)
        plt.text(0.5e-8,3.5e-13,r'{\bf Red giants}',fontsize=fs,color='w')

        # Solar neutrinos arXiv:[0807.2926]
        SolarNu_col = [0.01, 0.75, 0.24]
        SolarNu = loadtxt("limit_data/AxionElectron/SolarNu.txt")
        plt.plot(SolarNu[:,0],SolarNu[:,1],color='k',lw=2,alpha=0.7,zorder=1)
        plt.fill_between(SolarNu[:,0],SolarNu[:,1],y2=y2,edgecolor=None,facecolor=SolarNu_col,zorder=0.7)
        plt.text(0.5e-8,3.8e-11,r'{\bf Solar} $\nu$',fontsize=fs,color='w')

        if Hint:
            # White dwarf hint arXiv:[1708.02111]
            col = 'k'
            dat = loadtxt("limit_data/AxionElectron/WDhint.txt")
            plt.fill_between(dat[:,0],dat[:,1],color=col,edgecolor=None,lw=0.001,zorder=0.1,alpha=0.3)
            plt.text(5e-6,1.4e-13,r'{\bf White dwarf hint}',fontsize=fs-10)

#==============================================================================#
#==============================================================================#











#==============================================================================#
def MySaveFig(fig,pltname,pngsave=True):
    fig.savefig(pltdir+pltname+'.pdf',bbox_inches='tight')
    if pngsave:
        fig.savefig(pltdir_png+pltname+'.png',bbox_inches='tight')

def cbar(mappable,extend='neither',minorticklength=8,majorticklength=10,\
            minortickwidth=2,majortickwidth=2.5,pad=0.2,side="right",orientation="vertical"):
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(side, size="5%", pad=pad)
    cbar = fig.colorbar(mappable, cax=cax,extend=extend,orientation=orientation)
    cbar.ax.tick_params(which='minor',length=minorticklength,width=minortickwidth)
    cbar.ax.tick_params(which='major',length=majorticklength,width=majortickwidth)
    cbar.solids.set_edgecolor("face")

    return cbar

def MySquarePlot(xlab='',ylab='',\
                 lw=2.5,lfs=45,tfs=25,size_x=13,size_y=12,Grid=False):
    plt.rcParams['axes.linewidth'] = lw
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif',size=tfs)
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{mathpazo}']

    fig = plt.figure(figsize=(size_x,size_y))
    ax = fig.add_subplot(111)

    ax.set_xlabel(xlab,fontsize=lfs)
    ax.set_ylabel(ylab,fontsize=lfs)

    ax.tick_params(which='major',direction='in',width=2,length=13,right=True,top=True,pad=7)
    ax.tick_params(which='minor',direction='in',width=1,length=10,right=True,top=True)
    if Grid:
        ax.grid()
    return fig,ax

def MyDoublePlot(xlab1='',ylab1='',xlab2='',ylab2='',\
                 wspace=0.25,lw=2.5,lfs=45,tfs=25,size_x=20,size_y=11,Grid=False):
    plt.rcParams['axes.linewidth'] = lw
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif',size=tfs)
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{mathpazo}']
    fig, axarr = plt.subplots(1, 2,figsize=(size_x,size_y))
    gs = gridspec.GridSpec(1, 2)
    gs.update(wspace=wspace)
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax1.tick_params(which='major',direction='in',width=2,length=13,right=True,top=True,pad=7)
    ax1.tick_params(which='minor',direction='in',width=1,length=10,right=True,top=True)
    ax2.tick_params(which='major',direction='in',width=2,length=13,right=True,top=True,pad=7)
    ax2.tick_params(which='minor',direction='in',width=1,length=10,right=True,top=True)

    ax1.set_xlabel(xlab1,fontsize=lfs)
    ax1.set_ylabel(ylab1,fontsize=lfs)

    ax2.set_xlabel(xlab2,fontsize=lfs)
    ax2.set_ylabel(ylab2,fontsize=lfs)

    if Grid:
        ax1.grid()
        ax2.grid()
    return fig,ax1,ax2


def MyTriplePlot(xlab1='',ylab1='',xlab2='',ylab2='',xlab3='',ylab3='',\
                 wspace=0.25,lw=2.5,lfs=45,tfs=25,size_x=20,size_y=7,Grid=False):
    plt.rcParams['axes.linewidth'] = lw
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif',size=tfs)
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{mathpazo}']
    fig, axarr = plt.subplots(1, 3,figsize=(size_x,size_y))
    gs = gridspec.GridSpec(1, 3)
    gs.update(wspace=wspace)
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])

    ax1.tick_params(which='major',direction='in',width=2,length=13,right=True,top=True,pad=7)
    ax1.tick_params(which='minor',direction='in',width=1,length=10,right=True,top=True)

    ax2.tick_params(which='major',direction='in',width=2,length=13,right=True,top=True,pad=7)
    ax2.tick_params(which='minor',direction='in',width=1,length=10,right=True,top=True)

    ax3.tick_params(which='major',direction='in',width=2,length=13,right=True,top=True,pad=7)
    ax3.tick_params(which='minor',direction='in',width=1,length=10,right=True,top=True)

    ax1.set_xlabel(xlab1,fontsize=lfs)
    ax1.set_ylabel(ylab1,fontsize=lfs)

    ax2.set_xlabel(xlab2,fontsize=lfs)
    ax2.set_ylabel(ylab2,fontsize=lfs)

    ax3.set_xlabel(xlab3,fontsize=lfs)
    ax3.set_ylabel(ylab3,fontsize=lfs)

    if Grid:
        ax1.grid()
        ax2.grid()
        ax3.grid()
    return fig,ax1,ax2,ax3
#==============================================================================#


#==============================================================================#
def reverse_colourmap(cmap, name = 'my_cmap_r'):
    reverse = []
    k = []

    for key in cmap._segmentdata:
        k.append(key)
        channel = cmap._segmentdata[key]
        data = []

        for t in channel:
            data.append((1-t[0],t[2],t[1]))
        reverse.append(sorted(data))

    LinearL = dict(zip(k,reverse))
    my_cmap_r = mpl.colors.LinearSegmentedColormap(name, LinearL)
    return my_cmap_r
#==============================================================================#


#==============================================================================#
def col_alpha(col,alpha=0.1):
    rgb = colors.colorConverter.to_rgb(col)
    bg_rgb = [1,1,1]
    return [alpha * c1 + (1 - alpha) * c2
            for (c1, c2) in zip(rgb, bg_rgb)]
#==============================================================================#
