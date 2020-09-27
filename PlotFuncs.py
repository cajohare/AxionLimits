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

# Black hole superradiance constraints on the axion mass
# can be used for any coupling
def BlackHoleSpins(ax,label_position,fs=20,col='k',alpha=0.2,PlotLine=True,rotation=90,text_col='k'):
    y2 = ax.get_ylim()[-1]

    # arxiv: 2009.07206
    BH = loadtxt("limit_data/BlackHoleSpins.txt")
    if PlotLine:
        plt.plot(BH[:,0],BH[:,1],color=col,lw=3,alpha=min(alpha*2,1),zorder=0)
    plt.fill_between(BH[:,0],BH[:,1],y2=0,edgecolor=None,facecolor=col,zorder=0,alpha=alpha)
    plt.text(label_position[0],label_position[1],r'{\bf Black hole spins}',fontsize=fs,color=text_col,\
             rotation=rotation,ha='center',rotation_mode='anchor')

    return

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

            ax.tick_params(which='major',direction=tickdir,width=2.5,length=13,right=TopAndRightTicks,top=TopAndRightTicks,pad=8)
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
                          cmap='YlOrBr',fs=18,RescaleByMass=False,text_on=True,thick_lines=False):
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
                vmin = amax(QCD)/(C_logwidth/4.6)
                plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=0.9,zorder=0)
                plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=0.9,zorder=0)
                plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=0.9,zorder=0)

                # QCD Axion models
                rot = 45.0
                trans_angle = plt.gca().transData.transform_angles(array((rot,)),array([[0, 0]]))[0]
                m2 = array([1e-9,5e-8])
                if KSVZ_on:
                    if thick_lines:
                        plt.plot(m,g_x(KSVZ,m),'-',linewidth=5,color='k',zorder=0)
                        plt.plot(m,g_x(KSVZ,m),'-',linewidth=3,color=cols(0.7),zorder=0)
                    else:
                        plt.plot(m,g_x(KSVZ,m),'-',linewidth=2,color=cols(1.0),zorder=0)
                    if text_on:
                        plt.text(1e-8,g_x(KSVZ,1e-8)*1.05,r'{\bf KSVZ}',fontsize=fs,rotation=trans_angle,color=cols(1.0),ha='left',va='bottom',rotation_mode='anchor')
                if DFSZ_on:
                    if thick_lines:
                        plt.plot(m,g_x(DFSZ,m),'-',linewidth=5,color='k',zorder=0)
                        plt.plot(m,g_x(DFSZ,m),'-',linewidth=3,color=cols(0.7),zorder=0)
                    else:
                        plt.plot(m,g_x(DFSZ,m),'-',linewidth=2,color=cols(1.0),zorder=0)
                    if text_on:
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
                if thick_lines:
                    plt.plot([1e-9,1e0],[0.75,0.75],'-',lw=5,color='k')
                    plt.plot([1e-9,1e0],[0.75,0.75],'-',lw=3,color='k')
                else:
                    plt.plot([1e-9,1e0],[0.75,0.75],'-',lw=2,color='k')
                if text_on:
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
        dat = loadtxt("limit_data/AxionPhoton/ADMX_Sidecar.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)


        if projection:
            # ADMX arXiv[1804.05750]
            dat = loadtxt("limit_data/AxionPhoton/Projections/ADMX_Projected.txt")
            plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
            plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.1)
            if rs1==0:
                plt.text(1e-5,2.3e-16,r'{\bf ADMX}',fontsize=20,color=col,rotation=0,ha='left',va='top')
                plt.plot([3e-5,2e-5],[3e-16,0.6e-15],'k-',lw=1.5)
            else:
                plt.text(0.9e-6,0.15,r'{\bf ADMX}',fontsize=fs,color=col,rotation=0,ha='left',va='top')
        else:
            if rs1==0:
                plt.text(0.7e-6,1e-13,r'{\bf ADMX}',fontsize=fs,color=col,rotation=90,ha='left',va='top')

        return


    def NeutronStars(ax,col=[0.1, 0.5, 0.2],fs=17,RescaleByMass=False):
        # Neutron stars: Green Bank arXiv:[2004.00011]
        # Jansky VLA: 2008.01877, 2008.11188

        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt('limit_data/AxionPhoton/NeutronStars_GreenBank.txt')
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',alpha=0.5,lw=0.5,zorder=0)

        dat = loadtxt('limit_data/AxionPhoton/NeutronStars_VLA.txt')
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',alpha=0.5,lw=0.5,zorder=0)

        if rs1==0:
            plt.text(3e-6,0.8e-10,r'{\bf Neutron stars}',fontsize=fs,color='w',ha='left')
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
            plt.text(0.4e-5,0.6e-11,r'{\bf RBF+UF}',fontsize=fs,color='w',rotation=-90,ha='left',va='top')
        else:
            plt.text(0.7e-5,4e3,r'{\bf RBF}',fontsize=fs,color='w',rotation=0,ha='center',va='top')
            plt.text(0.7e-5,1e3,r'{\bf UF}',fontsize=fs,color='w',rotation=0,ha='center',va='top')

        return

    def HAYSTAC(ax,col=[0.88, 0.07, 0.37],fs=13,RescaleByMass=False,projection=True):
        # HAYSTAC arXiv:[1803.03690] and [2008.01853]
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
        dat2 = loadtxt("limit_data/AxionPhoton/HAYSTAC_2020.txt")

        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=3)
            plt.plot([dat2[0,0],dat2[0,0]],[dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),y2/(rs1*2e-10*dat2[0,0]+rs2)],color=col,zorder=zo,lw=3)

            if projection==False:
                plt.text(2.4e-5,5e-13,r'{\bf HAYSTAC}',fontsize=fs,color=col,rotation=-90,ha='left',va='top')
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',zorder=zo,lw=4)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=3)
            plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)

            plt.plot([dat2[0,0],dat2[0,0]],[dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),y2/(rs1*2e-10*dat2[0,0]+rs2)],color='k',zorder=zo,lw=4)
            plt.plot([dat2[0,0],dat2[0,0]],[dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),y2/(rs1*2e-10*dat2[0,0]+rs2)],color=col,zorder=zo,lw=3)
            plt.text(dat2[0,0]*1.1,y2*1.2,r'{\bf HAYSTAC}',fontsize=fs,color=col,rotation=40,ha='left',rotation_mode='anchor')
            plt.plot(dat2[0,0],dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)
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
            plt.text(5.2e-5,0.8e-11,r'{\bf QUAX}',fontsize=fs,color=col,rotation=-90,ha='center',va='top')
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',lw=4,zorder=zo)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=3,zorder=zo)
            plt.text(dat[0,0]*1.1,y2*1.2,r'{\bf QUAX}',fontsize=fs,color=col,rotation=40,ha='left',rotation_mode='anchor')
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
            plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.2)
            if rs1==0:
                plt.text(5e-4,1.15e-14,r'{\bf ORGAN}',fontsize=18,color=col,rotation=0,ha='left',va='top')
                plt.plot([5e-4,1.5e-4],[1.3e-14,6e-13],'k-',lw=1.5)
            else:
                plt.text(1.2e-4,1e3,r'{\bf ORGAN}',fontsize=18,color='darkred',rotation=-90,ha='left',va='top')

        else:
            if rs1==0:
                plt.text(110e-6,1e-11,r'{\bf ORGAN}',fontsize=fs,color=col,rotation=-90,ha='left',va='top')
        return

    def MADMAX(ax,col='darkred',fs=18,RescaleByMass=False):
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
            plt.text(5e-5,3.5e0,r'{\bf MADMAX}',fontsize=14,color=col,rotation=0,ha='left',va='top')
        return


    def PlasmaHaloscope(ax,col='darkred',fs=18,RescaleByMass=False):
        # Plasma Haloscope arXiv[1904.11872]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/PlasmaHaloscope.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=2,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.2)
        if rs1==0:
            plt.text(1.5e-4,1e-15,r'{\bf Plasma haloscope}',fontsize=18,color=col,rotation=0,ha='left',va='top')
            plt.plot([1.3e-4,0.5e-4],[1e-15,0.7e-14],'k-',lw=1.5)
        else:
            plt.text(2.3e-4,5e-1,r'{\bf Plasma}',fontsize=fs,color=col,rotation=0,ha='center',va='top')
            plt.text(2.3e-4,2e-1,r'{\bf haloscope}',fontsize=fs,color=col,rotation=0,ha='center',va='top')
        return

    def KLASH(ax,col=[0.6, 0.1, 0.2],fs=15,RescaleByMass=False):
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
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,facecolor=col,zorder=0,alpha=0.3)
        if rs1==0:
            plt.text(1e-7,1e-12,r'{\bf KLASH}',rotation=90,fontsize=fs,color=col,ha='left',va='top')
        else:
            plt.text(2.5e-7,1.3e0,r'{\bf KLASH}',rotation=90,fontsize=fs,color=col,ha='left',va='top',rotation_mode='anchor')

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
            plt.text(0.6e-2,5e-14,r'{\bf TOORAD}',rotation=0,fontsize=18,color=col,ha='left',va='top')
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


    def UPLOAD(ax,col='tomato',fs=16):
        # UPLOAD arXiv:[1912.07751]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/UPLOAD.txt")
        n = shape(dat)[0]
        x = dat[arange(0,n,2),0]
        y = dat[arange(0,n,2),1]
        y[-1] = y2
        plt.plot(x,y,'k-',lw=1,zorder=10,alpha=0.9)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.8)
        #plt.text(0.8e-9,3e-8,r'{\bf UPLOAD}',fontsize=fs,color='w',rotation=-90,ha='center',va='top',zorder=9)
        return


    def ALPS(ax,projection=True,col=[0.8, 0.25, 0.33],fs=15,RescaleByMass=False):
        # ALPS-I arXiv:[1004.1313]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0

        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/ALPS.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',lw=2.5,zorder=1.53,alpha=0.5)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=1.53,lw=0.01)
        if rs1==0:
            plt.text(1e-5,7e-8,r'{\bf ALPS-I}',fontsize=20,color='w')
        if projection:
            dat = loadtxt("limit_data/AxionPhoton/Projections/ALPS-II.txt")
            plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',lw=1.5,zorder=1.5,color='k',alpha=0.5)
            if RescaleByMass:
                plt.text(9e-4,2.5e3,r'{\bf ALPS-II}',fontsize=20,color='k',rotation=20,alpha=0.5)
            else:
                plt.text(1.5e-3,3e-9,r'{\bf ALPS-II}',rotation=60,fontsize=18,color='w',zorder=10)
        return

    def OSQAR(ax,col=[0.6, 0.2, 0.25],fs=15):
        # OSQAR arXiv:[]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/OSQAR.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',lw=2.5,zorder=1.52,alpha=0.5)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.52,lw=0.01)
        plt.text(1e-5,1.5e-8,r'{\bf OSQAR}',fontsize=17,color='w')
        return

    def PVLAS(ax,col=[0.4, 0.2, 0.2],fs=15):
        # PVLAS arXiv:[]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/PVLAS.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',lw=2.5,zorder=1.51,alpha=0.4)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.51,lw=0.01)
        plt.text(2e-3,9e-8,r'{\bf PVLAS}',fontsize=17,color='w',rotation=45)
        return


    def CROWS(ax,col=[0.7, 0.2, 0.2],fs=15):
        # CROWS arXiv:[1310.8098]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/CROWS.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',lw=2.5,zorder=1.54,alpha=0.4)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.54,lw=0.01)
        plt.text(1e-7,1.5e-7,r'{\bf CROWS}',fontsize=17,color='w',rotation=0)
        return


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
            plt.text(1e-1,1.5e-9,r'{\bf CAST}',fontsize=fs+4,color='w',rotation=0,ha='center',va='top')
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
                plt.text(0.7e-2,0.12e1,r'{\bf IAXO}',fontsize=fs,color=IAXO_col,rotation=-18)
        return


    def Haloscopes(ax,projection=True,fs=20):
        AxionPhoton.ADMX(ax,projection=projection,fs=fs)
        AxionPhoton.RBF_UF(ax,fs=fs-2)
        AxionPhoton.HAYSTAC(ax,projection=projection)
        AxionPhoton.ABRACADABRA(ax,fs=fs,projection=projection)
        AxionPhoton.SHAFT(ax)
        AxionPhoton.CAPP(ax,fs=fs-4)
        AxionPhoton.ORGAN(ax,projection=projection)
        AxionPhoton.UPLOAD(ax)

        if projection:
            AxionPhoton.PlasmaHaloscope(ax)
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
        AxionPhoton.ALPS(ax,projection=projection)
        AxionPhoton.OSQAR(ax)
        AxionPhoton.CROWS(ax)
        return


    def AstroBounds(ax,projection=True,fs=15):
        y2 = ax.get_ylim()[1]
        ### Astrophysical constraints

        # Fermi extragalactic SN gamma rays arXiv:[2006.06722]
        SNgamma_col = [0.05, 0.5, 0.06]
        SNgamma = loadtxt("limit_data/AxionPhoton/SNe-gamma.txt")
        plt.plot(SNgamma[:,0],SNgamma[:,1],'k-',alpha=0.6,zorder=0.25,lw=2)
        plt.fill_between(SNgamma[:,0],SNgamma[:,1],y2=y2,edgecolor=None,facecolor=SNgamma_col,zorder=0.25)
        plt.text(1.2e-12,0.51e-10,r'{\bf Fermi-SNe}',fontsize=fs-3,color='w',ha='left',va='top')

        # Diffuse SN ALP background arXiv:[2008.11741]
        DSNALP_col = [0.0, 0.62, 0.3]
        DSNALP = loadtxt("limit_data/AxionPhoton/DSNALP.txt")
        plt.plot(DSNALP[:,0],DSNALP[:,1],'k-',alpha=0.6,zorder=0.25,lw=2)
        plt.fill_between(DSNALP[:,0],DSNALP[:,1],y2=y2,edgecolor=None,facecolor=DSNALP_col,zorder=0.25)
        plt.text(1.2e-12,1.2e-10,r'{\bf DSNALP}',fontsize=fs-3,color='w',ha='left',va='top')


        # # SN1987 gamma rays arXiv:[1410.3747]
        SNgamma_col = [0.05, 0.5, 0.06]
        SNgamma = loadtxt("limit_data/AxionPhoton/SN1987A_gamma.txt")
        plt.plot(SNgamma[:,0],SNgamma[:,1],'k-',alpha=0.6,zorder=0.21,lw=2)
        plt.fill_between(SNgamma[:,0],SNgamma[:,1],y2=y2,edgecolor=None,facecolor=SNgamma_col,zorder=0.21)
        if projection==False:
            plt.text(6e-11,0.45e-11,r'{\bf SN1987A}',fontsize=fs,color=SNgamma_col,ha='left',va='top')

        # HYDRA-A arXiv:[1304.0989]
        HYDRA_col = [0.24, 0.71, 0.54]
        HYDRA = loadtxt("limit_data/AxionPhoton/HYDRA_A.txt")
        plt.plot(HYDRA[:,0],HYDRA[:,1],'k-',alpha=0.6,zorder=0.23,lw=2)
        plt.fill_between(HYDRA[:,0],HYDRA[:,1],y2=y2,edgecolor=None,facecolor=HYDRA_col,zorder=0.23)
        plt.text(1.2e-12,2e-11,r'{\bf Hydra}',fontsize=fs-2,color='w',ha='left',va='top')



        # M87 Limits from arXiv:[1703.07354]
        M87_col = 'seagreen'
        M87 = loadtxt("limit_data/AxionPhoton/M87.txt")
        plt.plot(M87[:,0],M87[:,1],'k-',lw=2,alpha=1,zorder=0.219)
        plt.fill_between(M87[:,0],M87[:,1],y2=y2,edgecolor=None,facecolor=M87_col,zorder=0.219)
        plt.text(1.4e-12,5e-12,r'\quad {\bf M87}',fontsize=fs,color='w',ha='left',va='top')

        # HESS arXiv:[1304.0700]
        HESS_col = [0.0, 0.55, 0.3]
        HESS = loadtxt("limit_data/AxionPhoton/HESS.txt")
        plt.plot(HESS[:,0],HESS[:,1],'k-',alpha=0.6,zorder=0.2,lw=2)
        plt.fill_between(HESS[:,0],HESS[:,1],y2=y2,edgecolor=None,facecolor=HESS_col,zorder=0.2)
        plt.text(2e-8,1.6e-11,r'{\bf HESS}',fontsize=fs+1,color=HESS_col,ha='left',va='top')

        # Mrk 421 arXiv:[2008.09464]
        Mrk_col = [0.4, 0.6, 0.1]
        Mrk = loadtxt("limit_data/AxionPhoton/Mrk421.txt")
        plt.plot(Mrk[:,0],Mrk[:,1],'k-',alpha=0.6,zorder=0.26,lw=2)
        plt.fill_between(Mrk[:,0],Mrk[:,1],y2=y2,edgecolor=None,facecolor=Mrk_col,zorder=0.26)
        plt.text(4e-9,1.2e-10,r'{\bf Mrk 421}',fontsize=fs-3,color='w',ha='left',va='top')

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

        # Telescopes (MUSE) [2009.01310]
        Telescopes_col1 = [0.09, 0.45, 0.27]
        Telescopes = loadtxt("limit_data/AxionPhoton/Telescopes_MUSE.txt")
        plt.fill_between(Telescopes[:,0],Telescopes[:,1],y2=y2,edgecolor=None,facecolor=Telescopes_col1,zorder=0.2)
        plt.text(1.5,0.7e-12,r'{\bf MUSE}',fontsize=fs,color=Telescopes_col1,rotation=90,ha='left',va='top',rotation_mode='anchor')

        # Telescopes (VIMOS) [astro-ph/0611502]
        Telescopes_col2 = [0.09, 0.6, 0.27]
        Telescopes = loadtxt("limit_data/AxionPhoton/Telescopes_VIMOS.txt")
        plt.fill_between(Telescopes[:,0],Telescopes[:,1],y2=y2,edgecolor=None,facecolor=Telescopes_col2,zorder=0.2)
        plt.text(7,1e-11,r'{\bf VIMOS}',fontsize=fs,color=Telescopes_col2,rotation=-90,ha='left',va='top')

        # Extra text:
        #plt.text(3,1.1e-13,r'{\bf Telescopes}',fontsize=fs,color=Telescopes_col1,rotation=0,ha='center',va='top')
        #plt.text(3,5e-14,r'(DM ALP decay)',fontsize=fs,color=Telescopes_col1,rotation=0,ha='center',va='top')

        # Chandra arXiv:[1907.05475]
        Chandra_col = [0.0, 0.3, 0.24]
        Chandra = loadtxt('limit_data/AxionPhoton/Chandra.txt')
        plt.plot(Chandra[:,0],Chandra[:,1],'k-',alpha=0.8,lw=2,zorder=0.1)
        plt.fill_between(Chandra[:,0],Chandra[:,1],y2=y2,edgecolor=None,facecolor=Chandra_col,zorder=0.1)
        if projection==False:
            plt.text(1.1e-11,2e-12,r'{\bf Chandra}',fontsize=fs,color=Chandra_col,rotation=0,ha='left',va='top')

        # Xray super star clusters arXiv:[2008.03305]
        col = [0.2, 0.54, 0.01]
        StarCluster = loadtxt("limit_data/AxionPhoton/Xray-SuperStarClusters.txt")
        plt.plot(StarCluster[:,0],StarCluster[:,1],'k-',alpha=0.6,zorder=0.22,lw=2)
        plt.fill_between(StarCluster[:,0],StarCluster[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.22)
        plt.text(2.2e-11,2.7e-11,r'{\bf Star}',fontsize=13,color='w',ha='left',va='top',rotation=45)
        plt.text(2.5e-11,2.7e-11,r'{\bf clusters}',fontsize=13,color='w',ha='left',va='top',rotation=45)



        if projection==True:
            # Fermi nearby SN prospects arXiv:[1609.02350]
            FermiSN = loadtxt("limit_data/AxionPhoton/Projections/FermiSN.txt")
            plt.fill_between(FermiSN[:,0],FermiSN[:,1],y2=y2,edgecolor=Fermi_col,linewidth=1.5,facecolor=Fermi_col,zorder=0.1,alpha=0.2)
            plt.text(1e-9,4e-12,r'{\bf Fermi SN}',fontsize=fs,color=Fermi_col,rotation=43,ha='left',va='top')


        return

    def Cosmology(ax,fs=30,projection=False):
        y2 = ax.get_ylim()[1]
        ## Cosmology constraints see arXiv:[1210.3196] for summary
        # Xray Background
        XRAY_col = [0.03, 0.57, 0.82]
        XRAY = loadtxt("limit_data/AxionPhoton/XRAY.txt")
        plt.plot(XRAY[:,0],XRAY[:,1],color='k',alpha=0.5,zorder=0.3,lw=2)
        plt.fill_between(XRAY[:,0],XRAY[:,1],y2=1e-11,edgecolor=None,facecolor=XRAY_col,zorder=0.3)
        if projection:
            # THESEUS 2008.08306
            THESEUS = loadtxt("limit_data/AxionPhoton/Projections/THESEUS.txt")
            plt.plot(THESEUS[:,0],THESEUS[:,1],color=XRAY_col,alpha=0.5,zorder=0.29,lw=2)
            plt.fill_between(THESEUS[:,0],THESEUS[:,1],y2=1e-11,edgecolor=None,alpha=0.1,facecolor=XRAY_col,zorder=0.29)
            plt.text(3e3,0.8e-18,r'{\bf THESEUS}',fontsize=17,color=XRAY_col,rotation=0,ha='right',va='top')
            plt.plot([3e3,5e3],[0.8e-18,1.3e-18],'k-')


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
            plt.text(0.8e-1,g_x(KSVZ,0.8e-1)*2.7,r'{\bf KSVZ}',fontsize=fs,rotation=trans_angle,color=col,ha='left',va='top',rotation_mode='anchor')
        if Hadronic_on:
            col = 'gold'
            plt.fill_between(m,g_x(Had_l,m),y2=g_x(Had_u,m),facecolor=col,zorder=0.01,alpha=0.6)
            plt.plot(m,g_x(Had_l,m),'k-',lw=3.5,zorder=0.01)
            plt.plot(m,g_x(Had_u,m),'k-',lw=3.5,zorder=0.01)
            plt.plot(m,g_x(Had_l,m),'-',lw=2,zorder=0.01,color=col)
            plt.plot(m,g_x(Had_u,m),'-',lw=2,zorder=0.01,color=col)
            plt.text(5e-3,g_x(Had_u,5e-3)/1.5,r'{\bf Hadronic models}',fontsize=fs-5,rotation=trans_angle,color='k',ha='left',va='top',rotation_mode='anchor')

        return

    def XENON1T(ax,col='crimson',fs=20):
        # XENON1T S2 analysis arXiv:[1907.11485]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/XENON1T_DM_S2.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=0.6,zorder=0.51,lw=2)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.51)

        # XENON1T S1+S2 analysis arXiv:[2006.09721]
        dat = loadtxt("limit_data/AxionElectron/XENON1T_DM_S1S2.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=0.6,zorder=0.51,lw=2)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.51)

        plt.text(1.2e2,4e-14,r'{\bf XENON1T}',fontsize=fs,color=col,ha='center',va='top')
        plt.text(1.2e2,2.5e-14,r'(DM)',fontsize=fs,color=col,ha='center',va='top')

        # Solar axion basin arXiv:[2006.12431]
        col = 'royalblue'
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/XENON1T_S2_SolarAxionBasin.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=0.6,zorder=0.6,lw=2)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.6)
        plt.text(3e3,2e-11,r'{\bf XENON1T}',fontsize=fs,color='k',ha='center',va='top')
        plt.text(3e3,1.3e-11,r'(Solar axion',fontsize=fs,color='k',ha='center',va='top')
        plt.text(3e3,0.8e-11,r' basin)',fontsize=fs,color='k',ha='center',va='top')

        return

    def LUX(ax,col='darkred',fs=20):
        # LUX arXiv:[1704.02297]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/LUX.txt")
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=0.6,zorder=0.52,lw=2)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.52)
        plt.text(0.2e-8,6e-12,r'{\bf LUX} (Solar axions)',fontsize=30,color='w',alpha=0.8,ha='left',va='top')
        return

    def PandaX(ax,col='firebrick',fs=20):
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

    def EDELWEISS(ax,col='darkred',projection=True,fs=20):
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

    def SuperCDMS(ax,col='maroon',fs=20):
        # SuperCDMS arXiv:[1911.11905]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/SuperCDMS.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.58)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=0.5,zorder=0.58,lw=3)
        plt.text(1.7e1,2.7e-11,r'{\bf SuperCDMS}',fontsize=fs-1,color='w',ha='left',va='top',alpha=0.8,rotation=-82)
        return

    def DARWIN(ax,col='brown',fs=20):
        # DARWIN arXiv:[1606.07001]
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

    def Magnon(ax,col='rebeccapurple',fs=20):
        # Axion-magnon conversion arXiv:[2005.10256]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/Projections/Magnon.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,color=col,alpha=0.4,zorder=0.51)
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=0.5,lw=3)
        plt.text(1.2e-6,1e-14,r'{\bf Magnons \newline (YIT, NiSP$_3$)}',fontsize=fs,color=col,ha='left',va='top',rotation=0)
        return

    def MagnonScan(ax,col='mediumvioletred',fs=20):
        # Axion-magnon conversion arXiv:[2005.10256 and 2001.10666]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionElectron/Projections/MagnonScan.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,color=col,alpha=0.4,zorder=0.51)
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=0.5,lw=3)
        plt.text(1.2e-5,0.5e-13,r'{\bf Magnons}',fontsize=fs-1,color=col,ha='center',va='top',rotation=0)
        plt.text(1.2e-5,0.7*0.5e-13,r'{\bf (Scanning)}',fontsize=fs-1,color=col,ha='center',va='top',rotation=0)

        return

    def UndergroundDetectors(ax,projection=True,fs=20):
        AxionElectron.LUX(ax,fs=fs)
        AxionElectron.PandaX(ax,fs=fs)
        AxionElectron.XENON1T(ax,fs=fs-2)
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
            AxionElectron.Magnon(ax,fs=fs)
            AxionElectron.MagnonScan(ax,fs=fs)
            #AxionElectron.ElectronSpinMagnetometers(ax)
        return

    def StellarBounds(ax,fs=30,Hint=True):
        y2 = ax.get_ylim()[1]
        # Stellar physics constraints
        # Red Giants arXiv:[2007.03694]
        RG_col = [0.0, 0.66, 0.42]
        dat = loadtxt("limit_data/AxionElectron/RedGiants.txt")
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=0.5,zorder=0.5,lw=2)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=RG_col,zorder=0.5)
        plt.text(0.2e-8,2e-13,r'{\bf Red giants} ($\omega$Cen)',fontsize=fs,color='w')

        # Solar neutrinos arXiv:[0807.2926]
        SolarNu_col = 'seagreen'
        SolarNu = loadtxt("limit_data/AxionElectron/SolarNu.txt")
        plt.plot(SolarNu[:,0],SolarNu[:,1],color='k',lw=2,alpha=0.7,zorder=1)
        plt.fill_between(SolarNu[:,0],SolarNu[:,1],y2=y2,edgecolor=None,facecolor=SolarNu_col,zorder=0.7)
        plt.text(0.2e-8,3.8e-11,r'{\bf Solar} $\nu$',fontsize=fs,color='w')

        if Hint:
            # White dwarf hint arXiv:[1708.02111]
            col = 'k'
            dat = loadtxt("limit_data/AxionElectron/WDhint.txt")
            plt.fill_between(dat[:,0],dat[:,1],color=col,edgecolor=None,lw=0.001,zorder=0.1,alpha=0.3)
            plt.text(1e-7,1e-13,r'{\bf White dwarf hint}',fontsize=fs-10)
#==============================================================================#


#==============================================================================#
class AxionNeutron():
    # Warning: often couplings are actually given as g_an/2 m_n (this is what is in the limit_data files)
    # But we are using the dimensionless coupling, so will multiply by the neutron mass
    # this makes essentially no observable difference to the plot but it useful to remember.
    m_n = 0.93957

    def FigSetup(xlab=r'$m_a$ [eV]',ylab='$|g_{an}|$',\
                     g_min = 1.0e-17,g_max = 1.0e-2,\
                     m_min = 1.0e-22,m_max = 1.0e-2,\
                     lw=2.5,lfs=45,tfs=25,tickdir='out',\
                     Grid=False,Shape='Rectangular',mathpazo=False,
                     TopAndRightTicks=False,FrequencyAxis=True):

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

            if FrequencyAxis:
                ax2 = ax.twiny()
                ax2.set_xlim([m_min*241.8*1e12,m_max*241.8*1e12])
                ax2.set_xlabel(r"$\nu_a$ [Hz]")
                ax2.set_xscale('log')
                plt.xticks(rotation=20)
                ax2.tick_params(which='major',direction=tickdir,width=2.5,length=13,pad=7)
                ax2.tick_params(which='minor',direction=tickdir,width=1,length=10)
                locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=50)
                locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10)*.1,numticks=100)
                ax2.xaxis.set_major_locator(locmaj)
                ax2.xaxis.set_minor_locator(locmin)
                ax2.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
                plt.sca(ax)
            return fig,ax

    def QCDAxion(ax,C_logwidth=10,KSVZ_on=True,DFSZ_on=True,
                      cmap='YlOrBr',fs=25):
        ## QCD Axion band:
        g_min,g_max = ax.get_ylim()
        m_min,m_max = ax.get_xlim()

        # Mass-coupling relation
        def g_x(C_ae,m_a):
            return 1.644e-7*C_ae*m_a
        DFSZ_l = 0.16
        DFSZ_u = 0.26

        plt.plot([3.5e-13,3.5e-13],[g_min,g_max],'k--',lw=3)
        plt.text(3.5e-13/4,1e-16,r'$f_a\sim M_{\rm Pl}$',fontsize=fs,rotation=90)

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
            plt.text(1e-8,g_x(DFSZ_u,1e-8)*5,r'{\bf DFSZ models}',fontsize=fs,rotation=trans_angle,color='k',ha='left',va='top',rotation_mode='anchor')
        return

    def OldComagnetometers(ax,col=[0.75, 0.2, 0.2],fs=20,projection=True):
        # Old comagnetometer data arXiv:[1907.03767]
        y2 = ax.get_ylim()[1]
        zo = 0.3
        dat = loadtxt("limit_data/AxionNeutron/OldComagnetometers.txt")
        dat[:,1] *= 2*AxionNeutron.m_n
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=2.5)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=1.0)
        plt.text(3e-15,4e-7,r'{\bf Old}',fontsize=fs,color='k',ha='center',va='top')
        plt.text(3e-15,1.5e-7,r'{\bf comagnetometers}',fontsize=fs,color='k',ha='center',va='top')
        if projection:
            dat = loadtxt("limit_data/AxionNeutron/Projections/FutureComagnetometers.txt")
            dat[:,1] *= 2*AxionNeutron.m_n
            plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=1,lw=3)
            plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.5)
            plt.text(5e-18,2*0.5e-12,r'{\bf Future comagnetometers}',fontsize=fs-1,color=col,ha='left',va='top')
        return

    def UltracoldNeutronsAndMercury(ax,col=[0.5, 0.0, 0.13],fs=20,projection=True):
        # arXiv:[1902.04644]
        StochasticCorrection = 18.0 #<---- From 1905.13650
        y2 = ax.get_ylim()[1]
        zo = 1
        dat = loadtxt("limit_data/AxionNeutron/UltracoldNeutronsAndMercury.txt")
        dat[:,1] *= 2*AxionNeutron.m_n
        plt.plot(dat[:,0],StochasticCorrection*dat[:,1],'-',color='k',alpha=0.5,zorder=zo,lw=3)
        plt.fill_between(dat[:,0],StochasticCorrection*dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.text(0.9e-19,2*StochasticCorrection*2.5e-5,r'$\nu_n/\nu_{\rm Hg}$',fontsize=fs,color='w',ha='left',va='top')
        return


    class CASPEr():
        def ZULF(ax,col=[0.6, 0.1, 0.1],fs=20,projection=True):
            # arXiv:[1902.04644]
            StochasticCorrection = 18.0 #<---- From 1905.13650
            y2 = ax.get_ylim()[1]
            zo = 1
            dat = loadtxt("limit_data/AxionNeutron/CASPEr_ZULF.txt")
            dat[:,1] *= 2*AxionNeutron.m_n
            plt.plot(dat[:,0],StochasticCorrection*dat[:,1],'-',color='k',alpha=1.0,zorder=zo,lw=0.5)
            plt.plot(dat[0:2,0],StochasticCorrection*dat[0:2,1],'k-',lw=2.5)
            plt.fill_between(dat[:,0],StochasticCorrection*dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=1.0)
            plt.text(0.3e-16,StochasticCorrection*0.95e-5,r'{\bf CASPEr-ZULF}',fontsize=fs-4,color='k',ha='left',va='top',rotation=40,rotation_mode='anchor')
            if projection:
                dat = loadtxt("limit_data/AxionNeutron/Projections/CASPEr_ZULF.txt")
                dat[:,1] *= 2*AxionNeutron.m_n
                plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=0.1,lw=3)
                plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.0,alpha=0.3)
                plt.text(1e-22,2*8e-11,r'{\bf CASPEr-ZULF} (projected)',fontsize=fs,color=col,ha='left',va='top')
            return

        def Comagnetometer(ax,col='darkred',fs=20,projection=True):
            # arXiv:[1901.10843]
            y2 = ax.get_ylim()[1]
            zo = 1.5
            dat = loadtxt("limit_data/AxionNeutron/CASPEr_Comagnetometer.txt")
            dat[:,1] *= 2*AxionNeutron.m_n
            plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=0.8,zorder=zo,lw=1.5)
            plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=1.0)
            plt.text(1e-21,1.5*5e-3,r'{\bf CASPEr-comag.}',fontsize=fs-1,color='w',ha='left',va='top')
            return

        def wind(ax,col='red',fs=20,projection=True):
            # arXiv:[1711.08999]
            y2 = ax.get_ylim()[1]
            zo = -1
            dat = loadtxt("limit_data/AxionNeutron/Projections/CASPEr_wind.txt")
            dat[:,1] *= 2*AxionNeutron.m_n
            plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=zo,lw=3)
            plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=0.5)
            plt.text(1.4e-9,2*1.1e-11,r'{\bf CASPEr}-wind',fontsize=fs,color=col,ha='left',va='top',rotation=27)
            return

    def LabExperiments(ax,projection=True,fs=20):
        y2 = ax.get_ylim()[1]

        # Long range spin dependent forces K-3He arXiv:[0809.4700]
        zo = 0.2
        col = [0.4, 0.2, 0.2]
        dat = loadtxt("limit_data/AxionNeutron/K-3He_Comagnetometer.txt")
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=0.5,zorder=zo,lw=3)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.text(2.0e-12,2e-4,r'{\bf K-}$^3${\bf He comagnetometer}',fontsize=fs,color='w',ha='left',va='top')

        # Torsion balance test of gravitational inverse square law: hep-ph/0611184
        # reinterpreted in: hep-ph/0611223
        zo = 0.21
        col = [0.2, 0.25, 0.25]
        dat = loadtxt("limit_data/AxionNeutron/TorsionBalance.txt")
        plt.fill_between(dat[:,0],dat[:,1]*11500,y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat[:,0],dat[:,1]*11500,'-',color='k',alpha=0.5,zorder=zo,lw=3)
        plt.text(1e-8,1.5e-3,r'{\bf Torsion balance}',fontsize=fs,color='w',ha='left',va='top')


        # SNO, axion-induced dissociation of deuterons  arXiv:[2004.02733]
        zo = 0.03
        col = 'darkred'
        dat = loadtxt("limit_data/AxionNeutron/SNO.txt")
        dat[:,1] *= 2*AxionNeutron.m_n
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=0.5,zorder=zo,lw=3)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.text(0.8e-2,4*1.6e-4,r'{\bf SNO}',fontsize=fs+6,color='w',ha='right',va='top')

        if projection:
            # Proton storage ring arXiv:[2005.11867]
            zo = -1
            col = 'crimson'
            dat = loadtxt("limit_data/AxionNeutron/Projections/StorageRing.txt")
            dat[:,1] *= 2*AxionNeutron.m_n
            plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=zo,lw=3)
            plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=0.3)
            plt.text(1.3e-22,2*4e-13,r'{\bf Proton Storage Ring}',fontsize=18,color=col,ha='left',va='top')


    def Haloscopes(ax,projection=True,fs=20):
        AxionNeutron.OldComagnetometers(ax,projection=projection,fs=fs)
        AxionNeutron.CASPEr.ZULF(ax,projection=projection,fs=fs)
        AxionNeutron.CASPEr.Comagnetometer(ax,projection=projection,fs=fs)
        AxionNeutron.UltracoldNeutronsAndMercury(ax,projection=projection,fs=fs+5)
        if projection:
            AxionNeutron.CASPEr.wind(ax,fs=fs)
        return

    def StellarBounds(ax,fs=30):
        y2 = ax.get_ylim()[1]

        # Stellar physics constraints
        # SN1987A cooling nucleon-nucleon Bremsstrahlung arXiv:[1906.11844]
        SN = loadtxt("limit_data/AxionNeutron/SN1987A.txt")
        SN[:,1] *= 2*AxionNeutron.m_n
        plt.fill_between(SN[:,0],SN[:,1],y2=y2,edgecolor=None,facecolor='ForestGreen',zorder=0.02)
        plt.plot(SN[:,0],SN[:,1],'k-',alpha=0.5,lw=2.5,zorder=0.02)
        plt.text(0.8e-2,2*2e-8,r'{\bf SN1987A}',fontsize=fs,color='w',ha='right',va='top')

        # Cooling of HESS J1731-347 arXiv:[1806.07991]
        SN = loadtxt("limit_data/AxionNeutron/NeutronStars.txt")
        SN[:,1] *= 2*AxionNeutron.m_n
        plt.fill_between(SN[:,0],SN[:,1],y2=y2,edgecolor=None,facecolor='DarkGreen',zorder=0.01)
        plt.plot(SN[:,0],SN[:,1],'k-',alpha=0.5,lw=2.5,zorder=0.01)
        plt.text(0.8e-2,9e-10,r'{\bf Neutron star cooling}',fontsize=fs-6,color='w',ha='right',va='top')
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



from matplotlib import patches
from matplotlib import text as mtext
import numpy as np
import math

class CurvedText(mtext.Text):
    """
    A text object that follows an arbitrary curve.
    """
    def __init__(self, x, y, text, axes, **kwargs):
        super(CurvedText, self).__init__(x[0],y[0],' ', **kwargs)

        axes.add_artist(self)

        ##saving the curve:
        self.__x = x
        self.__y = y
        self.__zorder = self.get_zorder()

        ##creating the text objects
        self.__Characters = []
        for c in text:
            if c == ' ':
                ##make this an invisible 'a':
                t = mtext.Text(0,0,'a')
                t.set_alpha(0.0)
            else:
                t = mtext.Text(0,0,c, **kwargs)

            #resetting unnecessary arguments
            t.set_ha('center')
            t.set_rotation(0)
            t.set_zorder(self.__zorder +1)

            self.__Characters.append((c,t))
            axes.add_artist(t)


    ##overloading some member functions, to assure correct functionality
    ##on update
    def set_zorder(self, zorder):
        super(CurvedText, self).set_zorder(zorder)
        self.__zorder = self.get_zorder()
        for c,t in self.__Characters:
            t.set_zorder(self.__zorder+1)

    def draw(self, renderer, *args, **kwargs):
        """
        Overload of the Text.draw() function. Do not do
        do any drawing, but update the positions and rotation
        angles of self.__Characters.
        """
        self.update_positions(renderer)

    def update_positions(self,renderer):
        """
        Update positions and rotations of the individual text elements.
        """

        #preparations

        ##determining the aspect ratio:
        ##from https://stackoverflow.com/a/42014041/2454357

        ##data limits
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()
        ## Axis size on figure
        figW, figH = self.axes.get_figure().get_size_inches()
        ## Ratio of display units
        _, _, w, h = self.axes.get_position().bounds
        ##final aspect ratio
        aspect = ((figW * w)/(figH * h))*(ylim[1]-ylim[0])/(xlim[1]-xlim[0])

        #points of the curve in figure coordinates:
        x_fig,y_fig = (
            np.array(l) for l in zip(*self.axes.transData.transform([
            (i,j) for i,j in zip(self.__x,self.__y)
            ]))
        )

        #point distances in figure coordinates
        x_fig_dist = (x_fig[1:]-x_fig[:-1])
        y_fig_dist = (y_fig[1:]-y_fig[:-1])
        r_fig_dist = np.sqrt(x_fig_dist**2+y_fig_dist**2)

        #arc length in figure coordinates
        l_fig = np.insert(np.cumsum(r_fig_dist),0,0)

        #angles in figure coordinates
        rads = np.arctan2((y_fig[1:] - y_fig[:-1]),(x_fig[1:] - x_fig[:-1]))
        degs = np.rad2deg(rads)


        rel_pos = 10
        for c,t in self.__Characters:
            #finding the width of c:
            t.set_rotation(0)
            t.set_va('center')
            bbox1  = t.get_window_extent(renderer=renderer)
            w = bbox1.width
            h = bbox1.height

            #ignore all letters that don't fit:
            if rel_pos+w/2 > l_fig[-1]:
                t.set_alpha(0.0)
                rel_pos += w
                continue

            elif c != ' ':
                t.set_alpha(1.0)

            #finding the two data points between which the horizontal
            #center point of the character will be situated
            #left and right indices:
            il = np.where(rel_pos+w/2 >= l_fig)[0][-1]
            ir = np.where(rel_pos+w/2 <= l_fig)[0][0]

            #if we exactly hit a data point:
            if ir == il:
                ir += 1

            #how much of the letter width was needed to find il:
            used = l_fig[il]-rel_pos
            rel_pos = l_fig[il]

            #relative distance between il and ir where the center
            #of the character will be
            fraction = (w/2-used)/r_fig_dist[il]

            ##setting the character position in data coordinates:
            ##interpolate between the two points:
            x = self.__x[il]+fraction*(self.__x[ir]-self.__x[il])
            y = self.__y[il]+fraction*(self.__y[ir]-self.__y[il])

            #getting the offset when setting correct vertical alignment
            #in data coordinates
            t.set_va(self.get_va())
            bbox2  = t.get_window_extent(renderer=renderer)

            bbox1d = self.axes.transData.inverted().transform(bbox1)
            bbox2d = self.axes.transData.inverted().transform(bbox2)
            dr = np.array(bbox2d[0]-bbox1d[0])

            #the rotation/stretch matrix
            rad = rads[il]
            rot_mat = np.array([
                [math.cos(rad), math.sin(rad)*aspect],
                [-math.sin(rad)/aspect, math.cos(rad)]
            ])

            ##computing the offset vector of the rotated character
            drp = np.dot(dr,rot_mat)

            #setting final position and rotation:
            t.set_position(np.array([x,y])+drp)
            t.set_rotation(degs[il])

            t.set_va('center')
            t.set_ha('center')

            #updating rel_pos to right edge of character
            rel_pos += w-used
