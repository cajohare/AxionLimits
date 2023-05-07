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
import matplotlib.patheffects as pe

pltdir = 'plots/'
pltdir_png = pltdir+'plots_png/'

#==============================================================================#
def col_alpha(col,alpha=0.1):
    rgb = colors.colorConverter.to_rgb(col)
    bg_rgb = [1,1,1]
    return [alpha * c1 + (1 - alpha) * c2
            for (c1, c2) in zip(rgb, bg_rgb)]
#==============================================================================#


def PlotBound(ax,filename,edgecolor='k',facecolor='crimson',alpha=1,lw=1.5,y2=1e10,zorder=0.1,
              linestyle='-',skip=1,FillBetween=True,edgealpha=1,rescale_m=False,
              scale_x=1,scale_y=1,start_x=0,end_x=nan,MinorEdgeScale=1.5,AddMinorEdges=False):
    dat = loadtxt(filename)
    if end_x/end_x==1:
        dat = dat[start_x:end_x,:]
    else:
        dat = dat[start_x:,:]
    dat[:,0] *= scale_x
    dat[:,1] *= scale_y
    if rescale_m:
        dat[:,1] = dat[:,1]/dat[:,0]
    if FillBetween:
        ax.fill_between(dat[0::skip,0],dat[0::skip,1],y2=y2,color=facecolor,alpha=alpha,zorder=zorder,lw=0)
    else:        
        ax.fill(dat[0::skip,0],dat[0::skip,1],color=facecolor,alpha=alpha,zorder=zorder,lw=0)
    ax.plot(dat[0::skip,0],dat[0::skip,1],color=edgecolor,zorder=zorder,lw=lw,linestyle=linestyle,alpha=edgealpha)
    if skip>1:
        ax.plot([dat[-2,0],dat[-1,0]],[dat[-2,1],dat[-1,1]],color=edgecolor,zorder=zorder,lw=lw,linestyle=linestyle,alpha=edgealpha)
    if AddMinorEdges:
        ax.plot([dat[-1,0],dat[-1,0]],[dat[-1,1],MinorEdgeScale*dat[-1,1]],color=edgecolor,zorder=zorder,lw=lw,linestyle=linestyle,alpha=edgealpha)
        ax.plot([dat[0,0],dat[0,0]],[dat[0,1],MinorEdgeScale*dat[0,1]],color=edgecolor,zorder=zorder,lw=lw,linestyle=linestyle,alpha=edgealpha)
    return

def line_background(lw,col):
    return [pe.Stroke(linewidth=lw, foreground=col), pe.Normal()]



def FilledLimit(ax,dat,text_label='',col='ForestGreen',edgecolor='k',zorder=1,\
                    lw=2,y2=1e0,edgealpha=0.6,text_on=False,text_pos=[0,0],\
                    ha='left',va='top',clip_on=True,fs=15,text_col='k',rotation=0,facealpha=1,path_effects=None,textalpha=1):
    plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,alpha=facealpha,zorder=zorder)
    plt.plot(dat[:,0],dat[:,1],'-',color=edgecolor,alpha=edgealpha,zorder=zorder,lw=lw)
    if text_on:
        plt.text(text_pos[0],text_pos[1],text_label,fontsize=fs,color=text_col,\
            ha=ha,va=va,clip_on=clip_on,rotation=rotation,rotation_mode='anchor',path_effects=path_effects,alpha=textalpha)
    return

def UnfilledLimit(ax,dat,text_label='',col='ForestGreen',edgecolor='k',zorder=1,\
                    lw=2,y2=1e0,edgealpha=0.6,text_on=False,text_pos=[0,0],\
                    ha='left',va='top',clip_on=True,fs=15,text_col='k',rotation=0,facealpha=1,\
                     linestyle='--'):
    plt.plot(dat[:,0],dat[:,1],linestyle=linestyle,color=edgecolor,alpha=edgealpha,zorder=zorder,lw=lw)
    if text_on:
        plt.text(text_pos[0],text_pos[1],text_label,fontsize=fs,color=text_col,\
            ha=ha,va=va,clip_on=clip_on,rotation=rotation,rotation_mode='anchor')
    return

# Black hole superradiance constraints on the axion mass
# can be used for any coupling
def BlackHoleSpins(ax,C,label_position,whichfile='Mehta',fs=20,col='k',alpha=0.4,\
                   PlotLine=True,rotation=90,linecolor='k',facecolor='k',text_col='k',text_on=True,zorder=0.1):
    y2 = ax.get_ylim()[-1]

    # arxiv: 2009.07206
    # BH = loadtxt("limit_data/BlackHoleSpins.txt")
    # if PlotLine:
    #     plt.plot(BH[:,0],BH[:,1],color=col,lw=3,alpha=min(alpha*2,1),zorder=0)
    # plt.fill_between(BH[:,0],BH[:,1],y2=0,edgecolor=None,facecolor=col,zorder=0,alpha=alpha)
    # if text_on:
    #     plt.text(label_position[0],label_position[1],r'{\bf Black hole spins}',fontsize=fs,color=text_col,\
    #          rotation=rotation,ha='center',rotation_mode='anchor')

    # arxiv: 2011.11646
    dat = loadtxt('limit_data/fa/BlackHoleSpins_'+whichfile+'.txt')
    dat[:,1] = dat[:,1]*C
    plt.fill_between(dat[:,0],dat[:,1],y2=0,lw=3,alpha=alpha,color=facecolor,zorder=zorder)
    if PlotLine:
        plt.plot(dat[:,0],dat[:,1],'-',lw=3,alpha=0.7,color=linecolor,zorder=zorder)
    if text_on:
        plt.text(label_position[0],label_position[1],r'{\bf Black hole spins}',fontsize=fs,color=text_col,\
            rotation=rotation,ha='center',rotation_mode='anchor')

    return

def UpperFrequencyAxis(ax,N_Hz=1,tickdir='out',xtick_rotation=0,labelsize=25,xlabel=r"$\nu_a$ [Hz]",lfs=40,tick_pad=8,tfs=25,xlabel_pad=10):
    m_min,m_max = ax.get_xlim()
    ax2 = ax.twiny()
    ax2.set_xlabel(xlabel,fontsize=lfs,labelpad=xlabel_pad)
    ax2.set_xscale('log')
    plt.xticks(rotation=xtick_rotation)
    ax2.tick_params(labelsize=tfs)
    ax2.tick_params(which='major',direction=tickdir,width=2.5,length=13,pad=tick_pad)
    ax2.tick_params(which='minor',direction=tickdir,width=1,length=10)
    locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=50)
    locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10)*.1,numticks=100)
    ax2.xaxis.set_major_locator(locmaj)
    ax2.xaxis.set_minor_locator(locmin)
    ax2.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    ax2.set_xlim([m_min*241.8*1e12/N_Hz,m_max*241.8*1e12/N_Hz])
    plt.sca(ax)

def UpperFrequencyAxis_Simple(ax,tickdir='out',xtick_rotation=0,labelsize=25,xlabel=None,lfs=40,tick_pad=8,tfs=25,xlabel_pad=10):
    m_min,m_max = ax.get_xlim()
    ax2 = ax.twiny()
    ax2.set_xscale('log')
    ax2.set_xlabel(xlabel,fontsize=lfs,labelpad=xlabel_pad)
    ax2.tick_params(labelsize=tfs)
    ax2.tick_params(which='major',direction=tickdir,width=2.5,length=13,pad=tick_pad)
    ax2.tick_params(which='minor',direction=tickdir,width=1,length=10)
    locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=50)
    locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10)*.1,numticks=100)
    ax2.xaxis.set_major_locator(locmaj)
    ax2.xaxis.set_minor_locator(locmin)
    ax2.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    ax2.set_xticks(10.0**arange(-9,18))
    ax2.set_xticklabels(['nHz','','',r'\textmu Hz','','','mHz','','','Hz','','','kHz','','','MHz','','','GHz','','','THz','','','PHz','','']);
    ax2.set_xlim([m_min*241.8*1e12,m_max*241.8*1e12])
    plt.sca(ax)
    return

def AlternativeCouplingAxis(ax,scale=1,tickdir='out',labelsize=25,ylabel=r"$g_\gamma$ [GeV$^{-1}$]",lfs=40,tick_pad=8,tfs=25,ylabel_pad=60):
    g_min,g_max = ax.get_ylim()
    ax3 = ax.twinx()
    ax3.set_ylim([g_min*scale,g_max*scale])
    ax3.set_ylabel(ylabel,fontsize=lfs,labelpad=ylabel_pad,rotation=-90)
    ax3.set_yscale('log')
    ax3.tick_params(labelsize=tfs)
    ax3.tick_params(which='major',direction=tickdir,width=2.5,length=13,pad=tick_pad)
    ax3.tick_params(which='minor',direction=tickdir,width=1,length=10)
    locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=50)
    locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10)*.1,numticks=100)
    ax3.yaxis.set_major_locator(locmaj)
    ax3.yaxis.set_minor_locator(locmin)
    ax3.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    plt.sca(ax)

def FigSetup(xlab=r'$m_a$ [eV]',ylab='',\
                 g_min = 1.0e-19,g_max = 1.0e-6,\
                 m_min = 1.0e-12,m_max = 1.0e7,\
                 lw=2.5,lfs=45,tfs=25,tickdir='out',figsize=(16.5,11),\
                 Grid=False,Shape='Rectangular',\
                 mathpazo=False,TopAndRightTicks=False,majorticklength=13,minorticklength=10,\
                xtick_rotation=20.0,tick_pad=8,x_labelpad=10,y_labelpad=10,\
             FrequencyAxis=False,N_Hz=1,upper_xlabel=r"$\nu_a$ [Hz]",**freq_kwargs):

    plt.rcParams['axes.linewidth'] = lw
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif',size=tfs)

    if mathpazo:
            plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Palatino"],
            })

    if Shape=='Wide':
        fig = plt.figure(figsize=(16.5,5))
    elif Shape=='Rectangular':
        fig = plt.figure(figsize=(16.5,11))
    elif Shape=='Square':
        fig = plt.figure(figsize=(14.2,14))
    elif Shape=='Custom':
        fig = plt.figure(figsize=figsize)

    ax = fig.add_subplot(111)

    ax.set_xlabel(xlab,fontsize=lfs,labelpad=x_labelpad)
    ax.set_ylabel(ylab,fontsize=lfs,labelpad=y_labelpad)

    ax.tick_params(which='major',direction=tickdir,width=2.5,length=majorticklength,right=TopAndRightTicks,top=TopAndRightTicks,pad=tick_pad)
    ax.tick_params(which='minor',direction=tickdir,width=1,length=minorticklength,right=TopAndRightTicks,top=TopAndRightTicks)

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

    plt.xticks(rotation=xtick_rotation)

    if Grid:
        ax.grid(zorder=0)

    if FrequencyAxis:
        UpperFrequencyAxis(ax,N_Hz=N_Hz,tickdir='out',\
                           xtick_rotation=xtick_rotation,\
                           xlabel=upper_xlabel,\
                           lfs=lfs/1.3,tfs=tfs,tick_pad=tick_pad-2,**freq_kwargs)

    return fig,ax


#==============================================================================#
class AxionPhoton():
    def QCDAxion(ax,C_logwidth=10,KSVZ_on=True,DFSZ_on=True,cmap=cm.YlOrBr,fs=18,RescaleByMass=False,text_on=True,
                thick_lines=False,C_center=1,C_width=0.8,
                C_upper = 44/3-1.92,C_lower = abs(5/3-1.92),level_max = 4,nlevels=20,alpha=0.2,line_color='#a35c2f',
                KSVZ_label_mass=1e-8,DFSZ_label_mass=5e-8,vmax=0.9):
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
            # # Plot Band
            # n = 200
            # g = logspace(log10(g_min),log10(g_max),n)
            # m = logspace(log10(m_min),log10(m_max),n)
            # QCD = zeros(shape=(n,n))
            # for i in range(0,n):
            #     QCD[:,i] = norm.pdf(log10(g)-log10(g_x(C_center,m[i])),0.0,C_width)
            # cols = cm.get_cmap(cmap)

            # cols.set_under('w') # Set lowest color to white
            # vmin = amax(QCD)/(C_logwidth/4.6)
            # plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=vmax,zorder=0)
            # plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=vmax,zorder=0)
            # plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=vmax,zorder=0)

            # QCD axion hadronic band
            m = array([1e-30,1e20])
            ga = 2e-10*m
            cols = cmap(linspace(0.1,0.45,nlevels))
            levels = (linspace(1,sqrt(level_max),nlevels))**2
            for i in range(nlevels-1):
                ax.fill_between(m,C_upper*ga/levels[i],C_lower*ga*levels[i],alpha=alpha,color=cols[i,:],zorder=-1000,lw=0)

            # QCD Axion models
            rot = 45.0
            trans_angle = plt.gca().transData.transform_angles(array((rot,)),array([[0, 0]]))[0]
            m2 = array([1e-9,5e-8])
            if KSVZ_on:
                if thick_lines:
                    plt.plot(m,g_x(KSVZ,m),'-',linewidth=5,color='k',zorder=0)
                    plt.plot(m,g_x(KSVZ,m),'-',linewidth=3,color=line_color,zorder=0)
                else:
                    plt.plot(m,g_x(KSVZ,m),'-',linewidth=2,color=line_color,zorder=0)
                if text_on:
                    plt.text(KSVZ_label_mass,g_x(KSVZ,KSVZ_label_mass)*1.05,r'{\bf KSVZ}',fontsize=fs,rotation=trans_angle,color=line_color,ha='left',va='bottom',rotation_mode='anchor',clip_on=True)
            if DFSZ_on:
                if thick_lines:
                    plt.plot(m,g_x(DFSZ,m),'-',linewidth=5,color='k',zorder=0)
                    plt.plot(m,g_x(DFSZ,m),'-',linewidth=3,color=line_color,zorder=0)
                else:
                    plt.plot(m,g_x(DFSZ,m),'-',linewidth=2,color=line_color,zorder=0)
                if text_on:
                    plt.text(DFSZ_label_mass,g_x(DFSZ,DFSZ_label_mass)/1.5,r'{\bf DFSZ}',fontsize=fs,rotation=trans_angle,color=line_color,ha='left',va='top',rotation_mode='anchor',clip_on=True)
        else:
            # QCD axion hadronic band
            m = array([1e-30,1e20])
            ga = 2e-10*m
            cols = cmap(linspace(0.1,0.45,nlevels))
            levels = (linspace(1,sqrt(level_max),nlevels))**2
            for i in range(nlevels-1):
                ax.fill_between(m,C_upper/levels[i],C_lower*levels[i],alpha=alpha,color=cols[i,:],zorder=-1000,lw=0)

            if DFSZ_on:
                if thick_lines:
                    plt.plot([m_min,m_max],[0.75,0.75],'-',lw=5,color=line_color)
                    plt.plot([m_min,m_max],[0.75,0.75],'-',lw=3,color=line_color)
                else:
                    plt.plot([m_min,m_max],[0.75,0.75],'-',lw=2,color=line_color)
                if text_on:
                    plt.text(DFSZ_label_mass,0.75/3,r'{\bf DFSZ II}',fontsize=fs,color=line_color,clip_on=True)

            if KSVZ_on:
                if thick_lines:
                    plt.plot([m_min,m_max],[1.92,1.92],'-',lw=5,color=line_color)
                    plt.plot([m_min,m_max],[1.92,1.92],'-',lw=3,color=line_color)
                else:
                    plt.plot([m_min,m_max],[1.92,1.92],'-',lw=2,color=line_color)
                if text_on:
                    plt.text(KSVZ_label_mass,0.75/3,r'{\bf KSVZ}',fontsize=fs,color=line_color,clip_on=True)
        return

    def ADMX(ax,col=[0.8, 0.0, 0.0],projection=False,fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1],zorder=0.1):
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        # 2018: arXiv[1804.05750]
        # 2019: arXiv[1910.08638]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/ADMX.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=zorder)
        dat = loadtxt("limit_data/AxionPhoton/ADMX2018.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=zorder)
        dat = loadtxt("limit_data/AxionPhoton/ADMX2019_1.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=zorder)
        dat = loadtxt("limit_data/AxionPhoton/ADMX2019_2.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=zorder)
        dat = loadtxt("limit_data/AxionPhoton/ADMX2021.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=zorder)
        dat = loadtxt("limit_data/AxionPhoton/ADMX_Sidecar.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=zorder)


        if projection:
            # ADMX arXiv[1804.05750]
            dat = loadtxt("limit_data/AxionPhoton/Projections/ADMX_Projected.txt")
            plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
            plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.1)
            if text_on:
                if rs1==0:
                    plt.text(1e-5*text_shift[0],2.3e-16*text_shift[1],r'{\bf ADMX}',fontsize=20,color=col,rotation=0,ha='left',va='top',clip_on=True)
                    plt.plot([3e-5,2e-5],[3e-16,0.6e-15],'k-',lw=1.5)
                else:
                    plt.text(0.9e-6*text_shift[0],0.15*text_shift[1],r'{\bf ADMX}',fontsize=fs,color=col,rotation=0,ha='left',va='top',clip_on=True)
        else:
            if text_on:
                if rs1==0:
                    plt.text(0.85e-6*text_shift[0],1e-13*text_shift[1],r'{\bf ADMX}',fontsize=fs,color=col,rotation=90,ha='left',va='top',clip_on=True)
                else:
                    plt.gcf().text(0.39*text_shift[0],0.5*text_shift[1],r'{\bf ADMX}',rotation=90,color=col)
        return

    def RBF_UF(ax,col ='darkred',fs=13,RescaleByMass=False,text_on=True,text_shift=[1,1],zorder=0.1):
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
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=zorder)

        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*0.37e-5,text_shift[1]*0.8e-11,r'{\bf RBF+UF}',fontsize=fs,color='w',rotation=-90,ha='left',va='top',clip_on=True)
            else:
                plt.text(text_shift[0]*0.7e-5,text_shift[1]*4e3,r'{\bf RBF}',fontsize=fs,color='w',rotation=0,ha='center',va='top',clip_on=True)
                plt.text(text_shift[0]*0.7e-5,text_shift[1]*1e3,r'{\bf UF}',fontsize=fs,color='w',rotation=0,ha='center',va='top',clip_on=True)

        return

    def HAYSTAC(ax,col=[0.88, 0.07, 0.37],fs=13,RescaleByMass=False,projection=True,text_on=True,text_shift=[1,1]):
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
        dat3 = loadtxt("limit_data/AxionPhoton/HAYSTAC_2022.txt")

        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=2)
            plt.plot([dat2[0,0],dat2[0,0]],[dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),y2/(rs1*2e-10*dat2[0,0]+rs2)],color=col,zorder=zo,lw=2)
            plt.fill_between(dat3[:,0],dat3[:,1]/(rs1*2e-10*dat3[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=zo)
            if text_on:
                if projection==False:
                    plt.text(text_shift[0]*2.1e-5,text_shift[0]*5e-13,r'{\bf HAYSTAC}',fontsize=fs,color=col,rotation=-90,ha='left',va='top',clip_on=True)
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',zorder=zo,lw=4)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=3)
            plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)

            plt.plot([dat2[0,0],dat2[0,0]],[dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),y2/(rs1*2e-10*dat2[0,0]+rs2)],color='k',zorder=zo,lw=4)
            plt.plot([dat2[0,0],dat2[0,0]],[dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),y2/(rs1*2e-10*dat2[0,0]+rs2)],color=col,zorder=zo,lw=3)
            plt.text(text_shift[0]*dat2[0,0]*1.1,text_shift[1]*y2*1.2,r'{\bf HAYSTAC}',fontsize=fs,color=col,rotation=40,ha='left',rotation_mode='anchor')
            plt.plot(dat2[0,0],dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)
        return

    def TASEH(ax,col=[0.88, 0.07, 0.24],fs=13,RescaleByMass=False,projection=True,text_on=True,text_shift=[1,1]):
        # TASEH https://arxiv.org/pdf/2205.05574.pdf
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = 3
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = 0
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/TASEH.txt")

        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=2)
        return

    def CASTCAPP(ax,col=[0.88, 0.07, 0.24],fs=13,RescaleByMass=False,projection=True,text_on=True,text_shift=[1,1]):
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = 3
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = 0
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/CAST-CAPP.txt")

        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=2)
        return

    def CAPP(ax,col=[1, 0.1, 0.37],fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1]):
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = 3
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = 0
        dat = loadtxt("limit_data/AxionPhoton/CAPP-1.txt")
        dat2 = loadtxt("limit_data/AxionPhoton/CAPP-2.txt")
        dat3 = loadtxt("limit_data/AxionPhoton/CAPP-3.txt")
        dat4 = loadtxt("limit_data/AxionPhoton/CAPP-4.txt")
        dat5 = loadtxt("limit_data/AxionPhoton/CAPP-5.txt")
        dat6 = loadtxt("limit_data/AxionPhoton/CAPP-6.txt")

        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=3)
            plt.fill_between(dat2[:,0],dat2[:,1]/(rs1*2e-10*dat2[0,0]+rs2),y2=y2,color=col,zorder=zo)
            plt.fill_between(dat3[:,0],dat3[:,1]/(rs1*2e-10*dat3[0,0]+rs2),y2=y2,color=col,zorder=zo)
            plt.fill_between(dat4[:,0],dat4[:,1]/(rs1*2e-10*dat4[0,0]+rs2),y2=y2,color=col,zorder=zo)
            plt.fill_between(dat5[:,0],dat5[:,1]/(rs1*2e-10*dat5[0,0]+rs2),y2=y2,color=col,zorder=zo)
            plt.fill_between(dat6[:,0],dat6[:,1]/(rs1*2e-10*dat6[0,0]+rs2),y2=y2,color=col,zorder=zo)

            if text_on:
                plt.text(text_shift[0]*0.8e-5,text_shift[1]*0.1e-13,r'{\bf CAPP}',fontsize=fs,color=col,rotation=90,ha='center',va='top',clip_on=True)
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',zorder=zo,lw=4)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,zorder=zo,lw=3)
            if text_on:
                plt.text(text_shift[0]*dat[0,0]*1.1,text_shift[1]*y2*1.8,r'{\bf CAPP}',fontsize=fs,color=col,rotation=40,ha='left',va='top',rotation_mode='anchor')
            plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)
            imin = argmin(dat2[:,1])
            plt.plot(dat2[imin,0],dat2[imin,1]/(rs1*2e-10*dat2[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)
            imin = argmin(dat3[:,1])
            plt.plot(dat3[imin,0],dat3[imin,1]/(rs1*2e-10*dat3[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)
            plt.fill_between(dat2[:,0],dat2[:,1]/(rs1*2e-10*dat2[0,0]+rs2),y2=y2,color=col)
            plt.fill_between(dat3[:,0],dat3[:,1]/(rs1*2e-10*dat3[0,0]+rs2),y2=y2,color=col)
            plt.fill_between(dat4[:,0],dat4[:,1]/(rs1*2e-10*dat4[0,0]+rs2),y2=y2,color=col)
            plt.fill_between(dat5[:,0],dat5[:,1]/(rs1*2e-10*dat5[0,0]+rs2),y2=y2,color=col)
            plt.fill_between(dat6[:,0],dat6[:,1]/(rs1*2e-10*dat6[0,0]+rs2),y2=y2,color=col)
        return

    def QUAX(ax,col='crimson',fs=13,RescaleByMass=False,text_on=True,text_shift=[1,1],projection=False):
        # QUAX1 arXiv:[1903.06547]
        # QUAX2 arXiv:[2012.09498]
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
        dat2 = loadtxt("limit_data/AxionPhoton/QUAX2.txt")
        dat3 = loadtxt("limit_data/AxionPhoton/QUAX3.txt")

        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=2,zorder=zo)
            plt.plot([dat2[0,0],dat2[0,0]],[dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),y2/(rs1*2e-10*dat2[0,0]+rs2)],color=col,lw=2,zorder=zo)
            plt.plot([dat3[0,0],dat3[0,0]],[dat3[0,1]/(rs1*2e-10*dat3[0,0]+rs2),y2/(rs1*2e-10*dat3[0,0]+rs2)],color=col,lw=2,zorder=zo)
            if text_on:
                plt.text(text_shift[0]*6.3e-5,text_shift[1]*0.05e-11,r'{\bf QUAX}',fontsize=fs,color=col,rotation=-90,ha='center',va='top',clip_on=True)
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',lw=4,zorder=zo)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=3,zorder=zo)
            plt.plot([dat2[0,0],dat2[0,0]],[dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),y2/(rs1*2e-10*dat2[0,0]+rs2)],color='k',lw=4,zorder=zo)
            plt.plot([dat2[0,0],dat2[0,0]],[dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),y2/(rs1*2e-10*dat2[0,0]+rs2)],color=col,lw=3,zorder=zo)
            plt.plot([dat3[0,0],dat3[0,0]],[dat3[0,1]/(rs1*2e-10*dat3[0,0]+rs2),y2/(rs1*2e-10*dat3[0,0]+rs2)],color='k',lw=4,zorder=zo)
            plt.plot([dat3[0,0],dat3[0,0]],[dat3[0,1]/(rs1*2e-10*dat3[0,0]+rs2),y2/(rs1*2e-10*dat3[0,0]+rs2)],color=col,lw=3,zorder=zo)
            if text_on:
                plt.text(text_shift[0]*dat2[0,0]*1.2,text_shift[1]*y2*1.2,r'{\bf QUAX}',fontsize=fs,color=col,rotation=40,ha='left',rotation_mode='anchor')
            plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)
            plt.plot(dat2[0,0],dat2[0,1]/(rs1*2e-10*dat2[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)

        if projection==True:
            dat = loadtxt("limit_data/AxionPhoton/Projections/QUAX2005.txt")
            plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
            plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.2)
            if rs1==1.0:
                plt.text(2.5e-5,0.8e-1,r'{\bf QUAX}',color=col,fontsize=18)
                plt.plot([4.0e-5,4.0e-5],[2.2e-1,2.1e0],'k-',lw=1.5)
        return

    def ABRACADABRA(ax,col=[0.83, 0.07, 0.37],fs=15,projection=False,RescaleByMass=False,text_on=True,lw=1,text_shift=[1,1],edgealpha=1):
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
        plt.plot(x,y/(rs1*2e-10*x+rs2),'k-',lw=lw,zorder=2.01,alpha=edgealpha)


        dat = loadtxt("limit_data/AxionPhoton/ABRACADABRA_run2.txt")
        n = shape(dat)[0]
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=2.02)
        x = dat[arange(0,n,1),0]
        y = dat[arange(0,n,1),1]
        y[-1] = y2
        plt.plot(x,y/(rs1*2e-10*x+rs2),'k-',lw=lw,zorder=2.02,alpha=edgealpha)


        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*1.5e-9,text_shift[1]*3e-8,r'{\bf ABRA}',fontsize=fs,color='w',rotation=0,ha='center',va='top',zorder=10,clip_on=True,path_effects=line_background(1.5,'k'))
                plt.text(text_shift[0]*1.5e-9,text_shift[1]*1e-8,r'10 cm',fontsize=fs,color='w',rotation=0,ha='center',va='top',zorder=10,clip_on=True,path_effects=line_background(1.5,'k'))

        if projection:
            dat = loadtxt("limit_data/AxionPhoton/Projections/ABRACADABRA.txt")
            plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
            plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.1)
            if text_on:
                if rs1==0:
                    plt.text(text_shift[0]*5e-12,text_shift[1]*4e-18,r'{\bf ABRACADABRA}',fontsize=fs-1,color=col,rotation=13,ha='left',va='top',clip_on=True)
                else:
                    plt.text(text_shift[0]*1.3e-9,text_shift[1]*1.0e2,r'{\bf ABRACADABRA}',fontsize=fs-1,color=col,rotation=0,ha='left',va='top',clip_on=True)
                    plt.plot([dat[-1,0],dat[-1,0]],[dat[-1,1]/(rs1*2e-10*dat[-1,0]+rs2),1e6],lw=1.5,color=col,zorder=0)
        return

    def DMRadio(ax,col=[0.83, 0.07, 0.37],fs=23,text_on=True,RescaleByMass=False,lw=2,text_shift=[1,1],linestyle='-',rotation=90):
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt('limit_data/AxionPhoton/Projections/DMRadio.txt')
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),linestyle=linestyle,linewidth=2,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.1)
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*2e-10,text_shift[1]*0.05e-16,r'{\bf DM-Radio}',color='crimson',fontsize=20,rotation=rotation,clip_on=True)
            else:
                plt.text(text_shift[0]*5e-9,text_shift[1]*4.0e-1,r'{\bf DM-Radio}',fontsize=fs-1,color=col,rotation=0,ha='left',va='top',clip_on=True)
        return


    def SRF(ax,col=[0.83, 0.07, 0.37],fs=20,text_on=True,RescaleByMass=False,lw=2,text_shift=[1,1],linestyle='-',rotation=-40):
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt('limit_data/AxionPhoton/Projections/SRF.txt')
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),linestyle=linestyle,linewidth=2,color=col,zorder=0.0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.0,alpha=0.1)
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*1.5e-11,text_shift[1]*0.7e-18,r'{\bf SRF-m$^3$}',color='crimson',fontsize=20,rotation=rotation,clip_on=True)
            else:
                plt.text(text_shift[0]*5e-9,text_shift[1]*4.0e-1,r'{\bf SRF-m$^3$}',fontsize=fs-1,color=col,rotation=0,ha='left',va='top',clip_on=True)
        return

    def WISPLC(ax,col=[0.8, 0.07, 0.37],fs=15,text_on=True,RescaleByMass=False,lw=2,text_shift=[1,1],linestyle='-',rotation=14):
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt('limit_data/AxionPhoton/Projections/WISPLC.txt')
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),linestyle=linestyle,linewidth=2,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.1)
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*2e-11,text_shift[1]*8e-16,r'{\bf WISPLC}',color='crimson',fontsize=fs,rotation=rotation,clip_on=True)
            else:
                plt.text(text_shift[0]*1.5e-9,text_shift[1]*1.5e4,r'{\bf WISPLC}',fontsize=fs+1,color=col,rotation=-14,ha='left',va='top',clip_on=True)
        return

    def ORGAN(ax,col=[0.8, 0.0, 0.0],projection=False,fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1],lw=0.5):
        # ORGAN arXiv[1706.00209]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = 6
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = 0
        dat = loadtxt("limit_data/AxionPhoton/ORGAN.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=col,facecolor=col,zorder=0.1,lw=1)

        dat2 = loadtxt("limit_data/AxionPhoton/ORGAN-1a.txt")
        plt.fill_between(dat2[:,0],dat2[:,1]/(rs1*2e-10*dat2[:,0]+rs2),y2=y2,edgecolor='k',facecolor=col,zorder=0.1,lw=lw)

        if projection:
            dat = loadtxt("limit_data/AxionPhoton/Projections/ORGAN_Projected.txt")
            plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
            plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.2)
            if text_on:
                if rs1==0:
                    plt.text(text_shift[0]*5e-4,text_shift[1]*1.15e-14,r'{\bf ORGAN}',fontsize=18,color=col,rotation=0,ha='left',va='top',clip_on=True)
                    plt.plot([5e-4,1.5e-4],[1.3e-14,6e-13],'k-',lw=1.5)
                else:
                    plt.text(text_shift[0]*1.2e-4,text_shift[1]*1e3,r'{\bf ORGAN}',fontsize=18,color='darkred',rotation=-90,ha='left',va='top',clip_on=True)

        else:
            if RescaleByMass:
                plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',lw=4,zorder=zo)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=1,zorder=zo)
            if RescaleByMass:
                plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)
            if text_on:
                if rs1==0:
                    plt.text(text_shift[0]*110e-6,text_shift[1]*3e-11,r'{\bf ORGAN}',fontsize=fs,color=col,rotation=-90,ha='left',va='top',clip_on=True)
                else:
                    plt.text(text_shift[0]*dat[0,0]*1.1,text_shift[1]*y2*1.2,r'{\bf ORGAN}',fontsize=fs-3,color=col,rotation=40,ha='left',rotation_mode='anchor')
                    plt.text(text_shift[0]*6e-5,text_shift[1]*1e2,r'{\bf ORGAN}',fontsize=fs-6,color=col,rotation=90,ha='left',rotation_mode='anchor')
        return

    def RADES(ax,col='blueviolet',fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1]):
        # RADES 2104.13798
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = 6
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = 0
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/RADES.txt")

        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=2,zorder=zo)
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',lw=4,zorder=zo)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=3,zorder=zo)
            if text_on:
                plt.text(text_shift[0]*dat[0,0]*0.88,text_shift[1]*y2*1.2,r'{\bf RADES}',fontsize=fs,color=col,rotation=40,ha='left',rotation_mode='anchor')
            plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)

        return

    def GrAHal(ax,col='#b53e5a',fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1]):
        # Grenoble haloscope  2110.14406
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = 6
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = 0
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/GrAHal.txt")

        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=2,zorder=zo)
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',lw=4,zorder=zo)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=3,zorder=zo)
            if text_on:
                plt.text(text_shift[0]*dat[0,0]*0.88,text_shift[1]*y2*1.2,r'{\bf GrAHal}',fontsize=fs,color=col,rotation=40,ha='left',rotation_mode='anchor')
            plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)

        return

    def MADMAX(ax,col='darkred',fs=18,RescaleByMass=False,text_on=True,text_shift=[1,1]):
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
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*1.5e-4,text_shift[1]*4.5e-15,r'{\bf MADMAX}',fontsize=18,color=col,rotation=0,ha='left',va='top',clip_on=True)
                plt.plot([3e-4,1.3e-4],[5.5e-15,2.6e-14],'k-',lw=1.5)
            else:
                plt.text(text_shift[0]*5e-5,text_shift[1]*3.5e0,r'{\bf MADMAX}',fontsize=14,color=col,rotation=0,ha='left',va='top',clip_on=True)

        return

    def DALI(ax,col='darkred',fs=18,RescaleByMass=False,text_on=True,text_shift=[1,1]):
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/DALI.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=2,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.2)
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*1.0e-4,text_shift[1]*0.6e-15,r'{\bf DALI}',fontsize=18,color=col,rotation=0,ha='left',va='top',clip_on=True)
                plt.plot([0.9e-4,0.32e-4],[0.6e-15,0.4e-14],'k-',lw=1.5)
            else:
                plt.text(text_shift[0]*1.3e-4,text_shift[1]*6e-1,r'{\bf DALI}',fontsize=fs/1.3,color=col,rotation=20,ha='center',va='top',clip_on=True)
                #plt.text(2.3e-4,2e-1,r'{\bf haloscope}',fontsize=fs,color=col,rotation=0,ha='center',va='top')
        return

    def ALPHA(ax,col='darkred',fs=18,RescaleByMass=False,text_on=True,text_shift=[1,1]):
        # Plasma Haloscope arXiv[1904.11872]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/ALPHA.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=2,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.2)
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*1.4e-4,text_shift[1]*1.6e-15,r'{\bf ALPHA}',fontsize=18,color=col,rotation=0,ha='left',va='top',clip_on=True)
                plt.plot([1.4e-4,0.6e-4],[1.6e-15,0.9e-14],'k-',lw=1.5)
            else:
                plt.text(text_shift[0]*2.3e-4,text_shift[1]*5e-1,r'{\bf ALPHA}',fontsize=fs,color=col,rotation=0,ha='center',va='top',clip_on=True)
                #plt.text(2.3e-4,2e-1,r'{\bf haloscope}',fontsize=fs,color=col,rotation=0,ha='center',va='top')
        return

    def FLASH(ax,col='darkred',fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1]):
        # FLASH https://indico.cern.ch/event/1115163/
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/FLASH.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,facecolor=col,zorder=0,alpha=0.3)
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*2.5e-6,text_shift[1]*0.45e-16,r'{\bf FLASH}',fontsize=20,color=col,rotation=0,ha='left',va='top',clip_on=True)
                plt.plot([1.2e-6,2.5e-6],[5e-16,0.6e-16],'k-',lw=1.5)
            else:
                plt.text(text_shift[0]*3e-7,text_shift[1]*3e0,r'{\bf FLASH}',rotation=90,fontsize=fs,color=col,ha='left',va='top',rotation_mode='anchor',clip_on=True)
        return

    def CADEx(ax,col='firebrick',fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1]):
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/CADEx.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,facecolor=col,zorder=0,alpha=0.1)
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*1.1e-3,text_shift[1]*0.35e-13,r'{\bf CADEx}',fontsize=18,color=col,rotation=0,ha='left',va='top',clip_on=True)
                plt.plot([1.3e-3,0.4e-3],[0.45e-13,2e-12],'k-',lw=1.5)
            else:
                plt.text(text_shift[0]*5e-4,text_shift[1]*1e2,r'{\bf CADEx}',fontsize=fs,rotation=-90,color=col,clip_on=True)

        return

    def BRASS(ax,col='darkred',fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1]):
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
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*2.4e-3,text_shift[1]*0.98e-13,r'{\bf BRASS}',fontsize=18,color=col,rotation=0,ha='left',va='top',clip_on=True)
                plt.plot([2.1e-3,0.7e-3],[0.95e-13,1.9e-12],'k-',lw=1.5)
            else:
                plt.text(text_shift[0]*0.45e-3,text_shift[1]*1e1,r'{\bf BRASS}',fontsize=20,rotation=9,color=col,clip_on=True)

        return

    def BREAD(ax,col='firebrick',fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1]):
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/BREAD.txt")
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,facecolor=col,zorder=0,alpha=0.1)
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*7e-3,text_shift[1]*2.5e-13,r'{\bf BREAD}',fontsize=18,color=col,rotation=0,ha='left',va='top',clip_on=True)
                plt.plot([5.5e-3,3e-3],[1.9e-13,2.9e-13],'k-',lw=1.5)
            else:
                plt.text(text_shift[0]*2e-3,text_shift[1]*1e-1,r'{\bf BREAD}',fontsize=18,rotation=0,color=col,clip_on=True)

        return

    def TOORAD(ax,col=[0.8, 0.1, 0.2],fs=15,RescaleByMass=False,text_on=True,text_shift=[1,0.5]):
        # TOORAD arXiv[1807.08810]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/Projections/TOORAD.txt")
        dat[:,0] *= 1e-3
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,facecolor=col,zorder=0,alpha=0.1)
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*0.7e-2,text_shift[1]*3e-11,r'{\bf TOO}',fontsize=12,ha='center',color=col,clip_on=True)
                plt.text(text_shift[0]*0.7e-2,text_shift[1]*1.5e-11,r'{\bf RAD}',fontsize=12,ha='center',color=col,clip_on=True)
            else:
                #plt.text((1-0.05)*text_shift[0]*0.25e-2,(1+0.05)*text_shift[1]*0.3e2,r'{\bf TOORAD}',fontsize=18,rotation=-21,color='k',clip_on=True)
                plt.text(text_shift[0]*0.25e-2,text_shift[1]*0.3e2,r'{\bf TOORAD}',fontsize=18,rotation=-21,color=col,clip_on=True,path_effects=line_background(1,'k'))
        return

    def LAMPOST(ax,col=[0.8, 0.1, 0.2],fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1],rotation=55):
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
        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*1.55e-1,text_shift[1]*3.5e-11,r'{\bf LAMPOST}',rotation=rotation,fontsize=fs,color=col,ha='left',va='top',clip_on=True)
            else:
                plt.text(text_shift[0]*0.9e-1,text_shift[1]*1.9e-1,r'{\bf LAMPOST}',rotation=0,fontsize=fs,color=col,ha='left',va='top',clip_on=True)

        return

    # Low mass ALP haloscopes
    def DANCE(ax,col=[0.8, 0.1, 0.2],fs=14,text_on=True,text_pos=[1.5e-12,1.7e-13],linestyle='-',rotation=50):
        # DANCE arXiv[1911.05196]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/Projections/DANCE.txt")
        plt.plot(dat[:,0],dat[:,1],linestyle=linestyle,linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0,alpha=0.1)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf DANCE}',rotation=rotation,fontsize=fs,color=col,ha='left',va='top',clip_on=True)
        return

    def aLIGO(ax,col=[0.8, 0.1, 0.2],fs=15,text_on=True,text_pos=[0.2e-9,0.35e-13],linestyle='-',rotation=0):
        # aLIGO arXiv[1903.02017]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/Projections/aLIGO.txt")
        plt.plot(dat[:,0],dat[:,1],linestyle=linestyle,linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0,alpha=0.1)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf aLIGO}',rotation=rotation,fontsize=fs,color=col,ha='left',va='top',clip_on=True)
        return

    def ADBC(ax,col=[0.8, 0.1, 0.2],fs=14,text_on=True,text_pos=[2e-11,0.6e-12],rotation=26):
        # ADBC arXiv[1809.01656]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/Projections/ADBC.txt")
        plt.plot(dat[:,0],dat[:,1],'-',linewidth=1.5,color=col,zorder=0)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0,alpha=0.1)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf ADBC}',rotation=rotation,fontsize=fs,color=col,ha='left',va='top',clip_on=True)
        return

    def SHAFT(ax,col='red',fs=16,text_on=True,lw=1,text_pos=[0.8e-10,3e-10],rotation=0,zorder=1.8,edgealpha=1):
        # SHAFT arXiv:[2003.03348]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/SHAFT.txt")
        n = shape(dat)[0]
        x = dat[arange(0,n,2),0]
        y = dat[arange(0,n,2),1]
        y[-1] = y2
        plt.plot(x,y,'k-',lw=lw,zorder=1.81,alpha=edgealpha)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zorder)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf SHAFT}',fontsize=fs,color='w',rotation=rotation,ha='center',va='top',clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def UPLOAD(ax,col='tomato',fs=16,text_on=False):
        # UPLOAD arXiv:[1912.07751]
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/UPLOAD.txt")
        n = shape(dat)[0]
        x = dat[arange(0,n,2),0]
        y = dat[arange(0,n,2),1]
        y[-1] = y2
        plt.plot(x,y,'k-',lw=1,zorder=10,alpha=0.9)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.8)
        #if text_on:

        #    plt.text(0.8e-9,3e-8,r'{\bf UPLOAD}',fontsize=fs,color='w',rotation=-90,ha='center',va='top',zorder=9,clip_on=True)
        return


    def BASE(ax,col='crimson',fs=15,RescaleByMass=False,text_on=True,text_shift=[1,1],zorder=1.9,lw=2.5,arrow_on=True):
        # BASE https://inspirehep.net/literature/1843024
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = zorder
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = zorder
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/BASE.txt")

        if arrow_on:
            fig = plt.gcf()
            plt.arrow(0.265, 0.535, 0, 0.035, transform=fig.transFigure,figure=fig,
              length_includes_head=True,lw=1,
              head_width=0.007, head_length=0.016, overhang=0.13,
              edgecolor='crimson',facecolor='crimson',clip_on=True)

        if rs1==0:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=lw,zorder=zo)
            if text_on:
                plt.text(text_shift[0]*3e-9,text_shift[1]*1.e-12,r'{\bf BASE}',fontsize=fs,color=col,rotation=90,ha='center',va='top',clip_on=True)
        else:
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color='k',lw=lw+2,zorder=zo)
            plt.plot([dat[0,0],dat[0,0]],[dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),y2/(rs1*2e-10*dat[0,0]+rs2)],color=col,lw=lw+1,zorder=zo)
            if text_on:
                plt.text(text_shift[0]*dat[0,0]*1.2,text_shift[1]*y2*1.2,r'{\bf BASE}',fontsize=fs,color=col,rotation=40,ha='left',rotation_mode='anchor')
            plt.plot(dat[0,0],dat[0,1]/(rs1*2e-10*dat[0,0]+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zo)

        return

    def ADMX_SLIC(ax,col='crimson',fs=12,RescaleByMass=False,text_on=True,text_shift=[1,1],zorder=0.005):
        # ADMX SLIC https://arxiv.org/pdf/1911.05772.pdf
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
            zo = zorder
        else:
            rs1 = 0.0
            rs2 = 1.0
            zo = zorder
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/ADMX_SLIC.txt")
        x = mean(dat[:,0])
        y = amin(dat[:,1])
        if rs1==0:
            plt.plot([x,x],[y/(rs1*2e-10*x+rs2),y2/(rs1*2e-10*x+rs2)],color=col,lw=2,zorder=zorder)
            if text_on:
                plt.text(text_shift[0]*2.4e-7,text_shift[1]*0.2e-11,r'{\bf ADMX SLIC}',fontsize=fs,color=col,rotation=-90,ha='center',va='top',clip_on=True)
        else:
            plt.plot([x,x],[y/(rs1*2e-10*x+rs2),y2/(rs1*2e-10*x+rs2)],color='k',lw=4,zorder=zorder)
            plt.plot([x,x],[y/(rs1*2e-10*x+rs2),y2/(rs1*2e-10*x+rs2)],color=col,lw=3,zorder=zorder)
            if text_on:
                plt.text(text_shift[0]*x,text_shift[1]*y2*1.2,r'{\bf ADMX SLIC}',fontsize=fs,color=col,rotation=40,ha='left',rotation_mode='anchor')
            plt.plot(x,y/(rs1*2e-10*x+rs2),'.',markersize=15,color=col,markeredgecolor='k',zorder=zorder)

        return

    def ALPS(ax,projection=True,col=[0.8, 0.25, 0.33],fs=15,lw=1.5,RescaleByMass=False,text_on=True,lw_proj=1.5,lsty_proj='-',col_proj='k',text_shift_x=1,text_shift_y=1,block=True):
        # ALPS-I arXiv:[1004.1313]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0

        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionPhoton/ALPS.txt")

        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=1.53,lw=0.01)
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',lw=lw,zorder=1.53,alpha=1)
        if rs1==0:
            if text_on: plt.text(1e-5*text_shift_x,8e-8*text_shift_y,r'{\bf ALPS-I}',fontsize=20,color='w',clip_on=True,path_effects=line_background(1.5,'k'))
        if projection:
            dat = loadtxt("limit_data/AxionPhoton/Projections/ALPS-II.txt")
            if block:
                mask = dat[:,0]<0.85e-6
                dat[mask,0] = nan
            plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),linestyle=lsty_proj,lw=lw_proj,zorder=1.5,color=col_proj,alpha=0.5)
            if RescaleByMass:
                plt.text(9e-4*text_shift_x,2.5e3*text_shift_y,r'{\bf ALPS-II}',fontsize=20,color='k',rotation=20,alpha=0.5,clip_on=True)
            else:
                if text_on: plt.text(1.5e-3*text_shift_x,3e-9*text_shift_y,r'{\bf ALPS-II}',rotation=61,fontsize=18,color='w',zorder=10,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def SAPPHIRES(ax,text_label=r'{\bf SAPPHIRES}',rotation=-57,text_pos=[1.4e-2,1e-1],col=[0.8, 0.2, 0.25],text_col='w',fs=20,zorder=1.91,text_on=True,edgealpha=1,lw=1.5):
        # SAPPHIRES arXiv:[2105.01224]
        dat = loadtxt("limit_data/AxionPhoton/SAPPHIRES.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,rotation=rotation,path_effects=line_background(1.5,'k'))
        return


    def OSQAR(ax,text_label=r'{\bf OSQAR}',text_pos=[1e-5,3e-8],col=[0.6, 0.2, 0.25],text_col='w',fs=17,zorder=1.52,text_on=True,edgealpha=1,lw=1.5):
        # OSQAR arXiv:[]
        dat = loadtxt("limit_data/AxionPhoton/OSQAR.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def PVLAS(ax,text_label=r'{\bf PVLAS}',text_pos=[2e-3,1.2e-7],col=[0.4, 0.2, 0.2],text_col='w',fs=17,zorder=1.51,text_on=True,edgealpha=1,rotation=45,lw=1.5):
        # PVLAS arXiv:[]
        dat = loadtxt("limit_data/AxionPhoton/PVLAS.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,rotation=rotation,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def CROWS(ax,text_label=r'{\bf CROWS}',text_pos=[1e-7,2.5e-7],col=[0.7, 0.2, 0.2],text_col='w',fs=17,zorder=1.54,text_on=True,edgealpha=1,lw=1.5):
        # CROWS arXiv:[1310.8098]
        dat = loadtxt("limit_data/AxionPhoton/CROWS.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def Helioscopes(ax,col=[0.5, 0.0, 0.13],fs=25,projection=False,RescaleByMass=False,text_on=True):
        # CAST arXiv:[1705.02290]
        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        dat = loadtxt("limit_data/AxionPhoton/CAST_highm.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor='k',facecolor=col,zorder=1.49,lw=0.1)
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',lw=1.5,zorder=1.49,alpha=1)

        mf = dat[-3,0]
        gf = dat[-3,1]
        dat = loadtxt("limit_data/AxionPhoton/CAST.txt")
        plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor='none',facecolor=col,zorder=1.5,lw=0.1)
        plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',lw=1.5,zorder=1.5,alpha=1)

        gi = 10.0**interp(log10(mf),log10(dat[:,0]),log10(dat[:,1]))/(rs1*2e-10*mf+rs2)
        plt.plot([mf,mf],[gf,gi],'k-',lw=1.5,zorder=1.5)
        if text_on==True:
            if rs1==0:
                plt.text(1e-1,1.5e-9,r'{\bf CAST}',fontsize=fs+4,color='w',rotation=0,ha='center',va='top',clip_on=True,path_effects=line_background(1.5,'k'))
            else:
                plt.text(4e-2,5e3,r'{\bf CAST}',fontsize=fs+4,color='w',rotation=0,ha='center',va='top',clip_on=True,path_effects=line_background(1.5,'k'))

        if projection:
            # IAXO arXiv[1212.4633]
            IAXO_col = 'purple'
            IAXO = loadtxt("limit_data/AxionPhoton/Projections/IAXO.txt")
            plt.plot(IAXO[:,0],IAXO[:,1]/(rs1*2e-10*IAXO[:,0]+rs2),'--',linewidth=2.5,color=IAXO_col,zorder=0.001)
            plt.fill_between(IAXO[:,0],IAXO[:,1]/(rs1*2e-10*IAXO[:,0]+rs2),y2=y2,edgecolor=None,facecolor=IAXO_col,zorder=0,alpha=0.3)
            if text_on==True:
                if rs1==0:
                    plt.text(1e-2,3.3e-13,r'{\bf IAXO}',fontsize=23,color='purple',rotation=0,clip_on=True)
                    plt.plot([3e-3,0.8e-2],[4.0e-12,6e-13],'k-',lw=1.5)
                else:
                    plt.text(0.7e-2,0.12e1,r'{\bf IAXO}',fontsize=fs,color=IAXO_col,rotation=-18,clip_on=True)
        return

    def FermiSNe(ax,text_label=r'{\bf Fermi-SNe}',text_pos=[1.2e-12,0.45e-10],col='ForestGreen',text_col='w',fs=12,zorder=0.265,text_on=True,edgealpha=1,lw=1.5):
        # Fermi extragalactic SN gamma rays arXiv:[2006.06722]
        dat = loadtxt("limit_data/AxionPhoton/SNe-gamma.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1,'k'))
        return

    def DSNALP(ax,text_label=r'{\bf DSNALP}',text_pos=[1.2e-12,1.2e-10],col=[0.0, 0.62, 0.3],text_col='w',fs=12,zorder=0.27,text_on=True,edgealpha=1,lw=1.5):
        # Diffuse SN ALP background arXiv:[2008.11741]
        dat = loadtxt("limit_data/AxionPhoton/DSNALP.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1,'k'))
        return

    def SN1987A_gamma(ax,text_label=r'{\bf SN1987A}',text_pos=[6e-11,0.4e-11],col='#067034',text_col='#067034',fs=15,zorder=0.21,text_on=True,edgealpha=1,lw=1.5):
        # SN1987 gamma rays arXiv:[1410.3747]
        dat = loadtxt("limit_data/AxionPhoton/SN1987A_gamma.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def Hydra(ax,text_label=r'{\bf Hydra}',text_pos=[1.2e-12,2e-11],col=[0.24, 0.71, 0.54],text_col='w',fs=13,zorder=0.23,text_on=True,edgealpha=1,lw=1.5):
        # HYDRA-A arXiv:[1304.0989]
        dat = loadtxt("limit_data/AxionPhoton/Chandra_HYDRA_A.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1,'k'))
        return

    def M87(ax,text_label=r'\quad {\bf M87}',text_pos=[1.4e-12,4e-12],col='seagreen',text_col='w',fs=15,zorder=0.219,text_on=True,edgealpha=1,lw=1.5):
        # M87 Limits from arXiv:[1703.07354]
        dat = loadtxt("limit_data/AxionPhoton/Chandra_M87.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1,'k'))
        return

    def HESS(ax,text_label=r'{\bf HESS}',text_pos=[1.4e-8,1.6e-11],col='#2a5736',text_col='#2a5736',fs=14,zorder=0.255,text_on=True,edgealpha=1,lw=1.5):
        # HESS arXiv:[1304.0700]
        dat = loadtxt("limit_data/AxionPhoton/HESS.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def Mrk421(ax,text_label=r'{\bf Mrk 421}',text_pos=[4e-9,6e-11],col=[0.4, 0.6, 0.1],text_col='w',fs=12,zorder=0.26,text_on=True,edgealpha=1,lw=1.5):
        # Fermi
        dat = loadtxt("limit_data/AxionPhoton/Mrk421.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1,'k'))
        
        # MAGIC
        dat = loadtxt("limit_data/AxionPhoton/Mrk421-MAGIC.txt")
        FilledLimit(ax,dat,None,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1,'k'))
        return

    def NGC1275(ax,text_label=r'{\bf Chandra}',text_pos=[1.1e-12,1.5e-12],col='#195e3a',text_col='w',fs=11,zorder=0.1,text_on=True,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/AxionPhoton/Chandra_NGC1275.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1,'k'))
        return

    def H1821643(ax,text_label=r'{\bf Chandra}',text_pos=[1e-11,1.5e-12],col=[0.0, 0.3, 0.24],text_col=[0.0, 0.3, 0.24],fs=15,zorder=0.1,text_on=True,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/AxionPhoton/Chandra_H1821643.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def Fermi(ax,text_label=r'{\bf Fermi}',text_pos=[4.02e-10,1.2e-11],col=[0.0, 0.42, 0.24],text_col='w',fs=15,zorder=0.24,text_on=True,edgealpha=1,lw=1.5):
        # Fermi NGC1275 arXiv:[1603.06978]
        Fermi1 = loadtxt("limit_data/AxionPhoton/Fermi1.txt")
        Fermi2 = loadtxt("limit_data/AxionPhoton/Fermi2.txt")
        plt.fill_between(Fermi1[:,0],Fermi1[:,1],y2=1e0,edgecolor=col,facecolor=col,zorder=zorder,lw=0.001)
        plt.fill(Fermi2[:,0],1.01*Fermi2[:,1],edgecolor=col,facecolor=col,lw=0.001,zorder=zorder)
        Fermi1 = loadtxt("limit_data/AxionPhoton/Fermi_bound.txt")
        Fermi2 = loadtxt("limit_data/AxionPhoton/Fermi_hole.txt")
        plt.plot(Fermi1[:,0],Fermi1[:,1],'k-',alpha=edgealpha,lw=lw,zorder=zorder)
        plt.plot(Fermi2[:,0],Fermi2[:,1],'k-',alpha=edgealpha,lw=lw,zorder=zorder)
        if text_on:
            plt.text(text_pos[0],text_pos[1],text_label,fontsize=fs,color=text_col,ha='left',va='top',clip_on=True,path_effects=line_background(1,'k'))
        return

    def FermiQuasars(ax,text_label=r'{\bf Quasars}',text_pos=[1.15e-8,0.8e-11],col='ForestGreen',text_col='w',fs=12,zorder=0.1,text_on=True,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/AxionPhoton/FermiQuasars.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,rotation=30,path_effects=line_background(1,'k'))
        return


    def MWDPolarisation(ax,text_shift=[1,0.35],col='#32a852',text_col='#32a852',fs=14,zorder=0.01,projection=False,text_on=True,edgealpha=1,lw=1.5):
        # Upper limit on the axion-photon coupling from magnetic white dwarf polarization arXiv:[2203.04319]s
        dat = loadtxt("limit_data/AxionPhoton/MWDPolarisation.txt")
        FilledLimit(ax,dat,col=col,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)

        if text_on:
            if projection==False:
                plt.plot([3e-8,9.5e-8],[1e-12,0.75e-11],'-',lw=lw,color=col,path_effects=line_background(lw+1,'k'))
                plt.text(text_shift[0]*2.3e-8,text_shift[1]*0.28e-11/2,r'{\bf MWD}',fontsize=fs,color=text_col,rotation=0,ha='center',clip_on=True)
                plt.text(text_shift[0]*2.3e-8,text_shift[1]*0.16e-11/2,r'{\bf Polarisation}',fontsize=fs*0.85,color=text_col,rotation=0,ha='center',clip_on=True)
            else:
                plt.text(text_shift[0]*3.5e-7,text_shift[1]*0.6e-11/0.35,r'{\bf MWD Pol.}',fontsize=11,color='w',rotation=40,ha='center',clip_on=True,path_effects=line_background(1,'k'))
        return

    def PulsarPolarCap(ax,text_label=r'{\bf Pulsars}',text_pos=[1.9e-7,4e-12],col='#039614',text_col='w',fs=13,zorder=0.005,text_on=True,lw=1.5,rotation=-11,edgealpha=1):
        dat = loadtxt("limit_data/AxionPhoton/PulsarPolarCap.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,lw=lw,va='center',rotation=rotation,edgealpha=edgealpha,path_effects=line_background(1,'k'))
        return

    def HAWC(ax,text_label=r'{\bf HAWC}',text_pos=[0.9e-7,2.5e-11],col='#2b5e4e',text_col='#2b5e4e',fs=14,zorder=0.25,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        # HAWC TeV Blazars arXiv:[2203.04332]
        dat = loadtxt("limit_data/AxionPhoton/HAWC.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return


    def MWDXrays(ax,text_label=r'{\bf MWD X-rays}',text_pos=[1.5e-7,1.3e-10],col='#59c275',text_col='#59c275',fs=14,zorder=0.1,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        # Magnetic white dwarf chandra x-rays arXiv:[2104.12772]
        dat = loadtxt("limit_data/AxionPhoton/MWDXrays.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return


    def StarClusters(ax,text_pos=[2.2e-11,2.7e-11],col= [0.2, 0.54, 0.01],text_col='w',fs=13,zorder=0.22,rotation=45,text_on=True,edgealpha=1,lw=1.5):
        # Xray super star clusters arXiv:[2008.03305]
        dat = loadtxt("limit_data/AxionPhoton/Xray-SuperStarClusters.txt")
        FilledLimit(ax,dat,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=False,edgealpha=edgealpha,lw=lw)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf Star}',fontsize=fs,color=text_col,ha='left',va='top',rotation=rotation,clip_on=True,path_effects=line_background(1,'k'))
            plt.text(0.91*text_pos[0],text_pos[1],r'{\bf clusters}',fontsize=fs,color=text_col,ha='left',va='top',rotation=rotation,clip_on=True,path_effects=line_background(1,'k'))
        return

    def Fermi_GalacticSN(ax,text_label=r'{\bf Fermi SN}',text_pos=[1e-9,5e-13],col=[0.0, 0.42, 0.24],text_col=[0.0, 0.42, 0.24],fs=15,zorder=0.0,text_on=True,rotation=43,lw=1.5,facealpha=0.05,edgealpha=0.6):
        # Fermi nearby SN prospects arXiv:[1609.02350]
        dat = loadtxt("limit_data/AxionPhoton/Projections/FermiSN.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,lw=lw,rotation=rotation,facealpha=facealpha,edgealpha=edgealpha)
        return

    def MUSE(ax,text_label=r'{\bf MUSE}',text_pos=[1.5,0.7e-12],col='royalblue',text_col='royalblue',fs=15,zorder=0.01,text_on=True,lw=0):
        # Telescopes (MUSE) [2009.01310]
        dat = loadtxt("limit_data/AxionPhoton/Telescopes_MUSE.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,edgecolor=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,rotation=90,lw=lw,edgealpha=0)
        return

    def VIMOS(ax,text_label=r'{\bf VIMOS}',text_pos=[10,0.22e-11],col='#2b2259',text_col='#2b2259',fs=15,zorder=0.01,text_on=True,lw=0):
        # Telescopes (VIMOS) [astro-ph/0611502]
        dat = loadtxt("limit_data/AxionPhoton/Telescopes_VIMOS.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,edgecolor=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,rotation=-90,lw=lw,edgealpha=0)
        return

    def HST(ax,text_label=r'{\bf HST}',text_pos=[7,3.4e-11],col='darkblue',text_col='w',fs=11,zorder=1e-5,text_on=True,lw=1.5,edgealpha=1,edgecolor='k',rotation=0):
        # Telescopes (HST)
        dat = loadtxt("limit_data/AxionPhoton/HST.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,edgecolor=edgecolor,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,rotation=rotation,lw=lw,edgealpha=edgealpha,path_effects=line_background(1,'k'))
        return

    def GammaRayAttenuation(ax,text_label=r'{\bf $\gamma$}',text_pos=[12,1.1e-11],col=[0.0, 0.2, 0.6],text_col=[0.0, 0.2, 0.6],fs=13,zorder=1e-6,text_on=True,lw=1.5,edgealpha=1,edgecolor='k',rotation=0):
        # Gamma ray attentuation on EBL, ALP dark atter bound
        dat = loadtxt("limit_data/AxionPhoton/GammaRayAttenuation.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,edgecolor=edgecolor,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,rotation=rotation,lw=lw,edgealpha=edgealpha)
        return

    def SolarBasin(ax,text_label=r'{\bf Solar basin}',rotation=98,text_pos=[0.7e4,0.1e-11],col=[0.03, 0.42, 0.29],text_col='w',fs=15,zorder=0.01,text_on=True,lw=1.5,edgecolor='k'):
        dat = loadtxt("limit_data/AxionPhoton/SolarBasin.txt")
        dat = loadtxt("limit_data/AxionPhoton/SolarBasin_Beaufort.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,edgecolor=edgecolor,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,rotation=rotation,lw=lw,edgealpha=1,path_effects=line_background(1,'k'))
        return

    def LeoT(ax,text_label=r'{\bf Leo T}',text_pos=[0.7e2,0.29e-13],col='midnightblue',text_col='midnightblue',fs=15,zorder=0.00003,text_on=True,rotation=-55,edgealpha=1,lw=1.5):
        # anomalous gas heating in Leo T dwarf
        dat = loadtxt("limit_data/AxionPhoton/LeoT.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,rotation=rotation,edgealpha=edgealpha,lw=lw)
        return


    def THESEUS(ax,text_label=r'{\bf THESEUS}',text_pos=[7e2,0.8e-17],col=[0.03, 0.57, 0.82],edgecolor=[0.03, 0.57, 0.82],text_col=[0.03, 0.57, 0.82],fs=17,zorder=0.00001,text_on=True,lw=1.5,facealpha=0.1):
        # THESEUS 2008.08306
        dat = loadtxt("limit_data/AxionPhoton/Projections/THESEUS.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,edgecolor=edgecolor,edgealpha=1,fs=fs,zorder=zorder,text_on=text_on,lw=lw,ha='right',facealpha=facealpha)
        plt.plot([8e2,1.4e3],[0.8e-17,1.3e-17],'k-',lw=2.5)
        plt.plot([8e2,1.4e3],[0.8e-17,1.3e-17],'-',lw=2,color=col)
        return

    def eROSITA(ax,text_label=r'{\bf eROSITA}',text_pos=[2e3,0.3e-18],col=[0.03, 0.57, 0.82],edgecolor=[0.03, 0.57, 0.82],text_col=[0.03, 0.57, 0.82],fs=17,zorder=0.00001,text_on=True,lw=1.5,facealpha=0.1):
        # eROSITA 2103.13241
        dat = loadtxt("limit_data/AxionPhoton/Projections/eROSITA.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,edgecolor=edgecolor,edgealpha=1,fs=fs,zorder=zorder,text_on=text_on,lw=lw,ha='right',facealpha=facealpha)
        plt.plot([2.1e3,3.5e3],[0.3e-18,0.4e-18],'-',lw=2.5,color=col)
        plt.plot([2.1e3,3.5e3],[0.3e-18,0.4e-18],'-',lw=2,color=col)
        return

    def NuSTAR(ax,text_label=r'{\bf NuSTAR}',text_pos=[2e3,0.7e-18],col='#676fa3',edgecolor='k',text_col='#676fa3',fs=17,zorder=-1,text_on=True,lw=0.5,facealpha=1):
        dat = loadtxt("limit_data/AxionPhoton/NuSTAR.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,edgecolor=edgecolor,edgealpha=1,fs=fs,zorder=zorder,text_on=text_on,lw=lw,ha='right',facealpha=facealpha)
        plt.plot([2.2e3,25e3],[0.5e-18,0.7e-18],'-',lw=2,color=col,path_effects=line_background(3,'k'))
        return

    def XMMNewton(ax,text_label=r'{\bf XMM-Newton}',text_pos=[1e3,1.8e-18],col='#3b4ba1',edgecolor='k',text_col='#3b4ba1',fs=17,zorder=0.00001,text_on=True,lw=0.5,facealpha=1):
        dat = loadtxt("limit_data/AxionPhoton/XMM-Newton.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,edgecolor=edgecolor,edgealpha=1,fs=fs,zorder=zorder,text_on=text_on,lw=lw,ha='right',facealpha=facealpha)
        plt.plot([1.2e3,6e3],[1.3e-18,2e-18],'-',lw=2,color=col,path_effects=line_background(3,'k'))
        return

    def INTEGRAL(ax,text_label=r'{\bf INTEGRAL}',text_pos=[0.7e4,2.7e-19],col='#6a919e',edgecolor='k',text_col='#6a919e',fs=17,zorder=0.00001,text_on=True,lw=1.5,facealpha=1):
        dat = loadtxt("limit_data/AxionPhoton/INTEGRAL.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,edgecolor=edgecolor,edgealpha=1,fs=fs,zorder=zorder,text_on=text_on,lw=lw,ha='right',facealpha=facealpha)
        if text_on: 
            plt.plot([0.8e4,8e4],[1.9e-19,2.3e-19],'-',lw=2,color=col,path_effects=line_background(3,'k'))
        return

    def COBEFIRAS(ax,text_label=r'{\bf COBE/FIRAS}',text_pos=[0.45e2,4e-13],col='#234f8c',text_col='w',fs=13,zorder=0.0001,text_on=True,rotation=-46,lw=1.5,edgealpha=1):
        dat = loadtxt("limit_data/AxionPhoton/COBE-FIRAS.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,rotation=rotation,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return
    
    def CMBAnisotropies(ax,text_label=r'{\bf CMB}',text_pos=[1.8e2,1.4e-13],col='#234f8c',text_col='w',fs=16,zorder=0.0001,text_on=True,rotation=-53,lw=1.5,edgealpha=1):
        dat = loadtxt("limit_data/AxionPhoton/CMB_Anisotropies.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,rotation=rotation,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def IrreducibleFreezeIn(ax,text_label=r'{\bf Freeze-in}',text_pos=[1.3e6,7e-14],col='#376631',edgecolor='k',text_col='w',fs=24,zorder=0.009,text_on=True,lw=1.5,facealpha=1,rotation=-55,edgealpha=1):
        dat = loadtxt("limit_data/AxionPhoton/IrreducibleFreezeIn.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,
                    rotation=rotation,edgecolor=edgecolor,fs=fs,
                    zorder=zorder,text_on=text_on,lw=lw,ha='right',facealpha=facealpha,edgealpha=edgealpha,path_effects=line_background(1.5,'k'))
        return

    def BBN_10MeV(ax,text_label=r'{\bf BBN}',text_pos=[0.4e7,3e-12],col='#027034',text_col='w',fs=15,zorder=0.02,text_on=True,lw=1.5,rotation=-25.5,edgealpha=1):
        # Most conservative BBN bound from https://arxiv.org/pdf/2002.08370.pdf (reheating temp = 10 MeV)
        dat = loadtxt('limit_data/AxionPhoton/BBN_10MeV.txt')
        plt.fill(dat[:,0],dat[:,1],edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_pos[0],text_pos[1],text_label,fontsize=fs,color=text_col,rotation=rotation,ha='left',va='top',clip_on=True,path_effects=line_background(1,'k'))
        return


    def Cosmology(ax,fs=30,text_on=True,edgealpha=1,lw=1.5):
        ## Cosmology constraints see arXiv:[1210.3196] for summary
        # Xray Background
        dat = loadtxt("limit_data/AxionPhoton/XRAY.txt")
        FilledLimit(ax,dat,r'{\bf X-rays}',y2=1e-10,text_pos=[1e4,0.8e-16],col=[0.03, 0.57, 0.82],text_col='w',fs=fs,zorder=0.00002,text_on=text_on,rotation=-50,ha='left',va='top',edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))

        # Ionisation fraction
        dat = loadtxt("limit_data/AxionPhoton/x_ion.txt")
        FilledLimit(ax,dat,'',col=[0.27, 0.51, 0.71],text_col='k',fs=fs,zorder=0.001,text_on=False,edgealpha=edgealpha,lw=lw)
        if text_on:
            plt.text(100.5744*0.93,2e-11,r'{\bf Ionisation}',fontsize=fs-12,color='w',rotation=-90,ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))
            plt.text(40*0.93,2e-11,r'{\bf fraction}',fontsize=fs-12,color='w',rotation=-90,ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))

        # BBN+N_eff arXiv:[2002.08370]
        dat = loadtxt("limit_data/AxionPhoton/BBN_Neff.txt")
        FilledLimit(ax,dat,r'{\bf BBN}+$N_{\rm eff}$',text_pos=[3.5e5,1.5e-11],col='#17570a',text_col='w',fs=fs*0.9,zorder=0.001,text_on=text_on,rotation=-55,ha='left',va='top',edgealpha=0.5,lw=lw,path_effects=line_background(1.5,'k'))

        # Extragalactic background light
        EBL = loadtxt("limit_data/AxionPhoton/EBL.txt")
        #EBL2 = loadtxt("limit_data/AxionPhoton/EBL2.txt")
        FilledLimit(ax,EBL,r'{\bf EBL}',text_pos=[9e4,2.5e-16],col=[0.0, 0.2, 0.6],text_col='w',fs=fs+5,zorder=0.001,text_on=text_on,rotation=-55,ha='left',va='top',edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        #FilledLimit(ax,EBL2,'',col=[0.0, 0.2, 0.6],text_on=False,zorder=0.001,edgealpha=edgealpha,lw=lw)

        # Spectral distortions of CMB
        AxionPhoton.COBEFIRAS(ax,text_on=False,edgealpha=edgealpha,lw=lw)
        AxionPhoton.CMBAnisotropies(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)

        # Freezein
        AxionPhoton.IrreducibleFreezeIn(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)

        return

    def GlobularClusters(ax,text_label=r'{\bf Globular clusters}',text_pos=[1e0,1.1e-10],col=[0.0, 0.66, 0.42],text_col='w',fs=25,zorder=0.05,text_on=True,lw=1.5,edgealpha=1):
        # Globular clusters arXiv:[1406.6053]
        dat = loadtxt("limit_data/AxionPhoton/GlobularClusters.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,lw=lw,va='center',edgealpha=edgealpha,path_effects=line_background(1.5,'k'))
        return

    def GlobularClusters_R2(ax,text_label=r'{\bf Globular clusters ($R_2$)}',text_pos=[1e-3,5e-11],col=[0.0, 0.66, 0.42],text_col='w',fs=23,zorder=0.01,text_on=True,lw=1.5,edgealpha=1):
        # R2 parameter https://arxiv.org/pdf/2207.03102.pdf
        dat = loadtxt("limit_data/AxionPhoton/GlobularClusters-R2.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,lw=lw,va='center',edgealpha=edgealpha,path_effects=line_background(1.5,'k'))
        return

    def WhiteDwarfs(ax,text_label=r'\noindent {\bf White}\newline  {\bf dwarfs}',text_pos=[1.1e6,4e-8],col='#2ec763',text_col='w',fs=18,zorder=0.04,text_on=True,lw=1.5,rotation=87,edgealpha=1):
        dat = loadtxt("limit_data/AxionPhoton/WhiteDwarfs.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,lw=lw,va='center',rotation=rotation,edgealpha=edgealpha,path_effects=line_background(1.5,'k'))
        return

    def SolarNu(ax,text_label=r'{\bf Solar} $\nu$',text_pos=[1e1,2e-9],col='seagreen',text_col='w',fs=33,zorder=1,text_on=True,lw=1.5,edgealpha=1):
        # Solar neutrino B8 bound arXiv:[1501.01639]
        dat = loadtxt("limit_data/AxionPhoton/SolarNu.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on,lw=lw,va='center',edgealpha=edgealpha,path_effects=line_background(1.5,'k'))
        return

    def DiffuseGammaRays(ax,text_label=r'{\bf Diffuse}-$\gamma$',text_pos=[1.5e5,2.5e-10],col='#318c49',text_col='w',fs=18,zorder=0.0299,text_on=True,lw=1.5,rotation=0):
        # https://arxiv.org/pdf/2109.03244.pdf
        dat = loadtxt("limit_data/AxionPhoton/DiffuseGammaRays.txt")
        plt.fill(dat[:,0],dat[:,1],edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=1,zorder=zorder)
        if text_on:
            plt.text(text_pos[0],text_pos[1],text_label,fontsize=fs,color=text_col,rotation=rotation,ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def SNe_decay(ax,text_pos=[4.5e7,0.3e-8],text_label=r'{\bf Low-E SNe}',col='#15732e',text_col='w',fs=19,zorder=0.03,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/SNe-decay.txt")
        plt.fill(dat[:,0],dat[:,1],edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_pos[0],text_pos[1],text_label,fontsize=fs,color='w',rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def SN1987A_decay(ax,text_label=r'{\bf SN1987A} ($\gamma$)',text_pos=[1.5e5,0.7e-10],col='#067034',text_col='w',fs=15,zorder=0.029,text_on=True,lw=1.5,rotation=-25.5,edgealpha=1):
        dat = loadtxt('limit_data/AxionPhoton/SN1987A_decay.txt')
        plt.fill(dat[:,0],dat[:,1],edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_pos[0],text_pos[1],text_label,fontsize=fs,color=text_col,rotation=rotation,ha='left',va='top',clip_on=True,path_effects=line_background(1,'k'))
        return

    def SN1987A_HeavyALP_nu(ax,text_shift=[1,1.0],col='darkgreen',text_col='w',fs=16,zorder=0.03,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1):
        # https://arxiv.org/pdf/2109.03244.pdf
        dat = loadtxt("limit_data/AxionPhoton/SN1987A_HeavyALP_nu.txt")
        plt.fill(dat[:,0],dat[:,1],edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*1.8e6,text_shift[1]*5e-9,r'{\bf SN1987A}',fontsize=fs,color='w',rotation=0,ha='center',va='top',clip_on=True,path_effects=line_background(1,'k'))
            plt.text(text_shift[0]*1.8e6,text_shift[1]*2e-9,r'($\nu$)',fontsize=fs,color='w',rotation=0,ha='center',va='top',clip_on=True,path_effects=line_background(1,'k'))
        return

    def NeutronStars(ax,col='#2ab0a3',fs=14,RescaleByMass=False,text_on=True,text_shift=[1,1],lw=1,text_col='#52a178',xskip=3,edgealpha=1):
        # Neutron stars: Green Bank arXiv:[2004.00011]
        # Jansky VLA: 2008.01877, 2008.11188
        # Battye et al. []

        y2 = ax.get_ylim()[1]
        if RescaleByMass:
            rs1 = 1.0
            rs2 = 0.0
        else:
            rs1 = 0.0
            rs2 = 1.0
        # dat = loadtxt('limit_data/AxionPhoton/NeutronStars_GreenBank.txt')
        # plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        # plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',alpha=0.5,lw=0.5,zorder=0)
        #
        # dat = loadtxt('limit_data/AxionPhoton/NeutronStars_VLA.txt')
        # plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        # plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',alpha=0.5,lw=0.5,zorder=0)
        #
        # dat = loadtxt('limit_data/AxionPhoton/NeutronStars_Battye.txt')
        # plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        # plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',alpha=0.5,lw=0.5,zorder=0)

        dat = loadtxt('limit_data/AxionPhoton/NeutronStars_BreakthroughListen.txt')
        plt.fill_between(dat[0::xskip,0],dat[0::xskip,1]/(rs1*2e-10*dat[0::xskip,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        plt.plot(dat[0::xskip,0],dat[0::xskip,1]/(rs1*2e-10*dat[0::xskip,0]+rs2),'k-',alpha=edgealpha,lw=lw,zorder=0.1)
        if (xskip>1)&(rs1==0.0):
            plt.plot([dat[-2,0],dat[-1,0]],[dat[-2,1],dat[-1,1]],'k-',alpha=edgealpha,lw=lw,zorder=0.1)

        dat = loadtxt('limit_data/AxionPhoton/NeutronStars_Battye2.txt')
        plt.fill_between(dat[0::xskip,0],dat[0::xskip,1]/(rs1*2e-10*dat[0::xskip,0]+rs2),y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        plt.plot(dat[0::xskip,0],dat[0::xskip,1]/(rs1*2e-10*dat[0::xskip,0]+rs2),'k-',alpha=edgealpha,lw=lw,zorder=0.1)
        if (xskip>1)&(rs1==0.0):
            plt.plot([dat[-2,0],dat[-1,0]],[dat[-2,1],dat[-1,1]],'k-',alpha=edgealpha,lw=lw,zorder=0.1)

        if text_on:
            if rs1==0:
                plt.text(text_shift[0]*1e-5,text_shift[1]*0.62e-10,r'{\bf Neutron stars}',fontsize=fs,color=text_col,ha='left',va='bottom')
            else:
                plt.text(text_shift[0]*1e-7,text_shift[1]*4e3,r'{\bf Neutron}',fontsize=fs,color=col,ha='center')
                plt.text(text_shift[0]*1e-7,text_shift[1]*1e3,r'{\bf stars}',fontsize=fs,color=col,ha='center')
                plt.plot([3.5e-7*text_shift[0],2e-5],[6e3*text_shift[1],8e3],lw=1.5,color=col,path_effects=line_background(2,'w'))
        return

    def AxionStarExplosions(ax,text_label=r'{\bf Axion star explosions}',text_pos=[4e-11,1.8e-12],col='#016682',rotation=27,text_col='w',fs=12,zorder=0.001,text_on=True,edgealpha=1,lw=1.5):
        # Axion star explosions - assumes 100% dark matter and a certain core-soliton mass relation
        dat = loadtxt('limit_data/AxionPhoton/AxionStarExplosions-1.txt')
        plt.fill(dat[:,0],dat[:,1],color=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',lw=lw,zorder=zorder,alpha=edgealpha)
        dat = loadtxt('limit_data/AxionPhoton/AxionStarExplosions-2.txt')
        plt.fill(dat[:,0],dat[:,1],color=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',lw=lw,zorder=zorder,alpha=edgealpha)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf Axion star}',fontsize=fs,color=text_col,rotation=rotation,ha='center',rotation_mode='anchor',path_effects=line_background(1,'k'),clip_on=True)
            plt.text(text_pos[0]*0.8,text_pos[1]/2,r'{\bf explosions}',fontsize=fs,color=text_col,rotation=rotation,ha='center',rotation_mode='anchor',path_effects=line_background(1,'k'),clip_on=True)
        return

    def BeamDump(ax,text_shift=[1,1],col='purple',text_col='w',fs=21,zorder=1.1,text_on=True,lw=1.5,rotation=-30,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/BeamDump.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*0.3e8,text_shift[1]*1e-4,r'{\bf Beam dump}',fontsize=fs,color='w',rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return


    def CMS_PbPb(ax,text_shift=[1,1],col='#851077',text_col='w',fs=17,zorder=0.2,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/CMS_PbPb.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*1.5e10,text_shift[1]*7e-4,r'{\bf CMS}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def ATLAS_PbPb(ax,text_shift=[1,1],col='#9732a8',text_col='#9732a8',fs=17,zorder=0.1,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=[]):
        dat = loadtxt("limit_data/AxionPhoton/ATLAS_PbPb.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)
        
        if text_on:
            plt.text(text_shift[0]*1.3e10,text_shift[1]*4e-5,r'{\bf ATLAS}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def LHC_pp(ax,text_shift=[1,1],col='#a11366',text_col='#a11366',fs=17,zorder=0.1,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=[]):
        dat = loadtxt("limit_data/AxionPhoton/LHC_pp.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*4.5e11,text_shift[1]*2.15e-5,r'{\bf LHC ($pp$)}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def NOMAD(ax,text_shift=[1,1],col='#96062a',text_col='w',fs=20,zorder=1.9,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/NOMAD.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*1e1,text_shift[1]*8e-4,r'{\bf NOMAD}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def BaBar(ax,text_shift=[1,1],col='#7a113d',text_col='w',fs=25,zorder=1.65,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/BaBar.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*1e6,text_shift[1]*0.5e-2,r'{\bf BaBar}',fontsize=fs,color='w',rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def LEP(ax,text_shift=[1,1],col='#824271',text_col='w',fs=25,zorder=0.9,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/LEP.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*0.6e9,text_shift[1]*2e-1,r'{\bf LEP}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def PrimEx(ax,text_shift=[1,1],col='#582078',text_col='#582078',fs=15,zorder=0.1,text_on=True,lw=1.5,rotation=-70,ha='center',edgealpha=1,path_effects=line_background(3,'w')):
        dat = loadtxt("limit_data/AxionPhoton/PrimEx.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*1.4e8,text_shift[1]*0.99e-3,r'{\bf PrimEx}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def BelleII(ax,text_shift=[1,1],col='#7a4282',text_col='w',fs=13.5,zorder=0.1,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/BelleII.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*0.6e9,text_shift[1]*5e-3,r'{\bf Belle II}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def BESIII(ax,text_shift=[1,1],col='#7a2282',text_col='#7a2282',fs=15.5,zorder=0.0,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=[]):
        dat = loadtxt("limit_data/AxionPhoton/BESIII.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*0.66e9,text_shift[1]*0.3e-3,r'{\bf BESIII}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def OPAL(ax,text_shift=[1,1],col='#6a113d',text_col='#6a113d',fs=11.5,zorder=0.0,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=[]):
        dat = loadtxt("limit_data/AxionPhoton/OPAL.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*2.6e9,text_shift[1]*0.1e-2,r'{\bf OPAL}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def Haloscopes(ax,projection=False,fs=20,text_on=True,BASE_arrow_on=True):
        AxionPhoton.ADMX(ax,projection=projection,fs=fs,text_on=text_on)
        AxionPhoton.HAYSTAC(ax,projection=projection,text_on=text_on)
        AxionPhoton.ABRACADABRA(ax,fs=fs,projection=False,text_on=text_on)
        AxionPhoton.SHAFT(ax,text_on=text_on)
        AxionPhoton.ORGAN(ax,projection=projection,text_on=text_on,lw=0)
        AxionPhoton.UPLOAD(ax,text_on=text_on)
        AxionPhoton.TASEH(ax,text_on=False)
        AxionPhoton.CASTCAPP(ax,text_on=False)

        if projection:
            AxionPhoton.CAPP(ax,fs=fs-4,text_on=False)
            AxionPhoton.RBF_UF(ax,fs=fs-2,text_on=False)
            AxionPhoton.DMRadio(ax,text_on=text_on)
            AxionPhoton.SRF(ax,text_on=text_on)
            AxionPhoton.ALPHA(ax,text_on=text_on)
            AxionPhoton.DALI(ax,text_on=text_on)
            AxionPhoton.MADMAX(ax,text_on=text_on)
            AxionPhoton.FLASH(ax,text_on=text_on)
            AxionPhoton.TOORAD(ax,text_on=text_on)
            AxionPhoton.BRASS(ax,text_on=text_on)
            AxionPhoton.BREAD(ax,text_on=text_on)
            AxionPhoton.CADEx(ax,text_on=text_on)
            AxionPhoton.ADBC(ax,text_on=text_on)
            AxionPhoton.DANCE(ax,text_on=text_on)
            AxionPhoton.aLIGO(ax,text_on=text_on)
            AxionPhoton.WISPLC(ax,text_on=text_on)
            AxionPhoton.LAMPOST(ax)

            AxionPhoton.ADMX(ax,text_on=False,col='darkred')
            AxionPhoton.CAPP(ax,text_on=False,col='darkred')
            AxionPhoton.ORGAN(ax,text_on=False,col='darkred',lw=0)
            AxionPhoton.HAYSTAC(ax,text_on=False,col='darkred')
            AxionPhoton.RBF_UF(ax,text_on=False,col='darkred')
            AxionPhoton.QUAX(ax,text_on=False,col='darkred')
            plt.text(0.5e-5,0.45e-12,r'{\bf Haloscopes}',color='w',rotation=90,fontsize=15)
        else:
            AxionPhoton.RBF_UF(ax,fs=fs-2,text_on=text_on)
            AxionPhoton.CAPP(ax,fs=fs-4,text_on=text_on)
            AxionPhoton.QUAX(ax,text_on=text_on)
            AxionPhoton.BASE(ax,text_on=text_on,arrow_on=BASE_arrow_on)
            AxionPhoton.ADMX_SLIC(ax,fs=fs-8,text_on=text_on)
            #AxionPhoton.RADES(ax,text_on=False)
            #AxionPhoton.GrAHal(ax,text_on=False)
        return

    def HaloscopesUniform(ax,projection=False,fs=20,text_on=True,col='darkred'):
        AxionPhoton.ADMX(ax,projection=projection,fs=fs,text_on=text_on,col=col)
        AxionPhoton.RBF_UF(ax,fs=fs-2,text_on=text_on,col=col)
        AxionPhoton.HAYSTAC(ax,projection=projection,text_on=text_on,col=col)
        AxionPhoton.ABRACADABRA(ax,fs=fs,projection=False,text_on=text_on,col=col,lw=0.75)
        AxionPhoton.SHAFT(ax,text_on=text_on,col=col,lw=0.75)
        AxionPhoton.CAPP(ax,fs=fs-4,text_on=text_on,col=col)
        AxionPhoton.ORGAN(ax,projection=projection,text_on=text_on,col=col,lw=0)
        AxionPhoton.UPLOAD(ax,text_on=text_on,col=col)
        AxionPhoton.QUAX(ax,text_on=text_on,col=col)
        AxionPhoton.BASE(ax,text_on=text_on,col=col,arrow_on=False)
        AxionPhoton.ADMX_SLIC(ax,fs=fs-8,text_on=text_on,col=col)
        AxionPhoton.RADES(ax,text_on=text_on,col=col)
        AxionPhoton.GrAHal(ax,text_on=text_on,col=col)
        return

    def LSW(ax,projection=False,text_on=True):
        AxionPhoton.ALPS(ax,projection=projection,text_on=text_on)
        AxionPhoton.PVLAS(ax,text_on=text_on)
        AxionPhoton.OSQAR(ax,text_on=text_on)
        AxionPhoton.CROWS(ax,text_on=text_on)
        return

    def ColliderBounds(ax,projection=False,text_on=True):
        AxionPhoton.BeamDump(ax,text_on=text_on)
        AxionPhoton.BaBar(ax,text_on=text_on)
        AxionPhoton.CMS_PbPb(ax,text_on=text_on)
        AxionPhoton.ATLAS_PbPb(ax,text_on=text_on)
        AxionPhoton.LHC_pp(ax,text_on=text_on)
        AxionPhoton.BelleII(ax,text_on=text_on)
        AxionPhoton.PrimEx(ax,text_on=text_on)
        AxionPhoton.LEP(ax,text_on=text_on)
        AxionPhoton.BESIII(ax,text_on=text_on)
        AxionPhoton.OPAL(ax,text_on=text_on)
        return

    def LowMassAstroBounds(ax,projection=False,text_on=True,edgealpha=1,lw=0.75,GalacticSN=False):
        AxionPhoton.FermiSNe(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
        AxionPhoton.DSNALP(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
        AxionPhoton.Hydra(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
        AxionPhoton.M87(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
        AxionPhoton.Mrk421(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
        AxionPhoton.Fermi(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
        AxionPhoton.StarClusters(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
        AxionPhoton.FermiQuasars(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
        if projection:
            AxionPhoton.NGC1275(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
            AxionPhoton.H1821643(ax,text_on=False,edgealpha=edgealpha,lw=lw)
            AxionPhoton.SN1987A_gamma(ax,text_on=False,edgealpha=edgealpha,lw=lw)
            if GalacticSN:
                AxionPhoton.Fermi_GalacticSN(ax,text_on=text_on,lw=lw)
            AxionPhoton.MWDXrays(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
            AxionPhoton.MWDPolarisation(ax,text_on=text_on,projection=True,edgealpha=edgealpha,lw=lw)
            AxionPhoton.PulsarPolarCap(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
            AxionPhoton.HESS(ax,text_on=False,edgealpha=edgealpha,lw=lw)
            AxionPhoton.HAWC(ax,text_on=False,edgealpha=edgealpha,lw=lw)
        else:
            AxionPhoton.NGC1275(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
            AxionPhoton.H1821643(ax,text_on=False,edgealpha=edgealpha,lw=lw)
            AxionPhoton.SN1987A_gamma(ax,text_on=False,edgealpha=edgealpha,lw=lw)
            AxionPhoton.HESS(ax,edgealpha=edgealpha,lw=lw,text_on=False)
            AxionPhoton.HAWC(ax,edgealpha=edgealpha,lw=lw,text_on=False)
            AxionPhoton.MWDXrays(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
            AxionPhoton.MWDPolarisation(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
            AxionPhoton.PulsarPolarCap(ax,text_on=text_on,edgealpha=edgealpha,lw=lw)
        return

    def StellarBounds(ax,text_on=True):
        AxionPhoton.GlobularClusters(ax,text_on=text_on)
        AxionPhoton.SolarNu(ax,text_on=text_on)
        AxionPhoton.WhiteDwarfs(ax,text_on=text_on)
        return

    def ALPdecay(ax,projection=False,text_on=True):
        AxionPhoton.DiffuseGammaRays(ax,text_on=text_on)
        AxionPhoton.SN1987A_decay(ax,text_on=text_on)
        AxionPhoton.SN1987A_HeavyALP_nu(ax,text_on=text_on)
        AxionPhoton.MUSE(ax,text_on=text_on)
        AxionPhoton.VIMOS(ax,text_on=text_on)
        AxionPhoton.HST(ax,text_on=text_on)
        AxionPhoton.GammaRayAttenuation(ax,text_on=text_on)
        AxionPhoton.XMMNewton(ax,text_on=text_on)
        AxionPhoton.INTEGRAL(ax,text_on=text_on)
        AxionPhoton.NuSTAR(ax,text_on=text_on)
        AxionPhoton.LeoT(ax,text_on=text_on)
        if projection:
            AxionPhoton.THESEUS(ax,text_on=text_on)
            #AxionPhoton.eROSITA(ax,text_on=text_on)
        return
        
    # ULTRALIGHT AXIONS:
    def SuperMAG(ax,text_shift=[1,1],col='red',text_col='w',fs=18,zorder=3,text_on=True,lw=1.5,rotation=-48,ha='center',edgealpha=1,path_effects=line_background(2,'k')):
        dat = loadtxt("limit_data/AxionPhoton/SuperMAG.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*1.7e-17,text_shift[1]*0.9e-9,r'{\bf SuperMAG}',fontsize=fs,color='w',rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def BICEPKECK(ax,text_shift=[1,1],col='#49548a',text_col='w',fs=20,zorder=1.2,text_on=True,lw=1.5,rotation=90,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/BICEP-KECK.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*2e-23,text_shift[1]*2e-11,r'{\bf BICEP/KECK}',fontsize=fs,color='w',rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return
    
    def POLARBEAR(ax,text_shift=[1,1],col='dodgerblue',text_col='w',fs=12,zorder=1.2,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/POLARBEAR.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*3.5e-22,text_shift[1]*0.5e-10,r'{\bf POLARBEAR}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return


    def MOJAVE(ax,text_shift=[1,1],col='royalblue',text_col='w',fs=20,zorder=1.2,text_on=True,lw=1.5,rotation=32,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/MOJAVE.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*3e-22,text_shift[1]*1.5e-11,r'{\bf MOJAVE}',fontsize=fs,color='w',rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def SPT(ax,text_shift=[1,1],col='#403c75',text_col='w',fs=18,zorder=1.01,text_on=True,lw=1.5,rotation=39,ha='center',edgealpha=1,path_effects=line_background(1.5,'k')):
        dat = loadtxt("limit_data/AxionPhoton/SPT.txt")
        dat[:,1] /= 1.1
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*1e-21,text_shift[1]*0.33e-11,r'{\bf SPT}',fontsize=fs,color='w',rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def PPA(ax,text_shift=[1,1],col='#403c75',text_col='#403c75',fs=18,zorder=0.1,text_on=True,lw=1.5,rotation=42,ha='center',edgealpha=1,path_effects=[]):
        dat = loadtxt("limit_data/AxionPhoton/Projections/PPA.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder,alpha=0.1)
        plt.plot(dat[:,0],dat[:,1],'--',lw=lw,color=col,alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*7e-21,text_shift[1]*4.5e-13,r'{\bf Pulsar polarisation array}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def PPTA_QUIJOTE(ax,text_shift=[1,1],col='darkblue',text_col='darkblue',fs=15,zorder=1.2,text_on=True,lw=1.5,rotation=39,ha='center',edgealpha=1,path_effects=[]):
        dat = loadtxt("limit_data/AxionPhoton/PPTA-QUIJOTE.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color='k',alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*1.5e-22,text_shift[1]*0.9e-12,r'{\bf PPTA+QUIJOTE}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return

    def TwistedAnyonCavity(ax,text_shift=[1,1],col='crimson',text_col='crimson',fs=22,zorder=0.1,text_on=True,lw=1.5,rotation=0,ha='center',edgealpha=1,path_effects=[]):
        dat = loadtxt("limit_data/AxionPhoton/Projections/TwistedAnyonCavity.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1,edgecolor=None,facecolor=col,zorder=zorder,alpha=0.2)
        plt.plot(dat[:,0],dat[:,1],'--',lw=lw,color=col,alpha=edgealpha,zorder=zorder)

        if text_on:
            plt.text(text_shift[0]*4e-20,text_shift[1]*0.7e-15,r'{\bf Twisted Anyon Cavity}',fontsize=fs,color=text_col,rotation=rotation,ha='center',va='top',clip_on=True,path_effects=path_effects)
        return
    
#==============================================================================#


#==============================================================================#
class AxionElectron():
    def QCDAxion(ax,text_on=True,C_logwidth=10,KSVZ_on=True,DFSZ_on=True,Hadronic_on=True,fs=25,DFSZ_col='gold',KSVZ_col='#857c20',Hadronic_col='goldenrod',DFSZ_label_mass=1e-4,KSVZ_label_mass=0.8e-1,Hadronic_label_mass=5e-3):
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
            col = DFSZ_col
            plt.fill_between(m,g_x(DFSZ_l,m),y2=g_x(DFSZ_u,m),facecolor=col,zorder=0,alpha=0.3)
            plt.plot(m,g_x(DFSZ_l,m),'k-',lw=3.5,zorder=0)
            plt.plot(m,g_x(DFSZ_u,m),'k-',lw=3.5,zorder=0)
            plt.plot(m,g_x(DFSZ_l,m),'-',lw=2,zorder=0,color=col)
            plt.plot(m,g_x(DFSZ_u,m),'-',lw=2,zorder=0,color=col)
            if text_on:
                plt.text(DFSZ_label_mass,g_x(DFSZ_u,DFSZ_label_mass)/1.5,r'{\bf DFSZ}',fontsize=fs,rotation=trans_angle,ha='left',va='top',rotation_mode='anchor',clip_on=True,color=DFSZ_col,path_effects=line_background(1,'k'))
        if KSVZ_on:
            col = KSVZ_col
            plt.plot(m,g_x(KSVZ,m),'-',lw=2,zorder=0.02,color=col)
            if text_on:
                plt.text(KSVZ_label_mass,g_x(KSVZ,KSVZ_label_mass)*2.1,r'{\bf KSVZ}',fontsize=fs*0.7,rotation=trans_angle,color=col,ha='left',va='top',rotation_mode='anchor',clip_on=True)
        if Hadronic_on:
            col = Hadronic_col
            plt.fill_between(m,g_x(Had_l,m),y2=g_x(Had_u,m),facecolor=col,zorder=0.01,alpha=0.25)
            plt.plot(m,g_x(Had_l,m),'k-',lw=3.5,zorder=0.01)
            plt.plot(m,g_x(Had_u,m),'k-',lw=3.5,zorder=0.01)
            plt.plot(m,g_x(Had_l,m),'-',lw=2,zorder=0.01,color=col)
            plt.plot(m,g_x(Had_u,m),'-',lw=2,zorder=0.01,color=col)
            if text_on:
                plt.text(Hadronic_label_mass,g_x(Had_u,Hadronic_label_mass)/1.5,r'{\bf Hadronic models}',fontsize=fs-5,rotation=trans_angle,ha='left',va='top',rotation_mode='anchor',clip_on=True,color=Hadronic_col,path_effects=line_background(1,'k'))

        return

    def XENON1T(ax,col='darkred',fs=19,text_on=True,zorder=0.51,lw=1.5,text_shift=[1,1],**kwargs):
        # XENON1T S2 analysis arXiv:[1907.11485]
        dat = loadtxt("limit_data/AxionElectron/XENON1T_DM_S2.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=1,zorder=zorder,lw=lw)

        # XENON1T S1+S2 analysis arXiv:[2006.09721]
        dat = loadtxt("limit_data/AxionElectron/XENON1T_DM_S1S2.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=1,zorder=zorder,lw=lw)

        # XENON1T Single electron analysis arXiv:[2112.12116]
        dat = loadtxt("limit_data/AxionElectron/XENON1T_DM_SE.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=1,zorder=zorder,lw=lw)

        if text_on:
            plt.text(text_shift[0]*1.2e2,text_shift[1]*4e-14,r'{\bf XENON1T}',fontsize=fs,color=col,ha='center',va='top',clip_on=True,**kwargs)
            #plt.text(text_shift[0]*1.2e2,text_shift[1]*2.5e-14,r'(DM)',fontsize=fs,color=col,ha='center',va='top',clip_on=True,**kwargs)
        return

    def XENONnT(ax,col='darkred',fs=19,text_on=True,zorder=0.51,lw=1.5,text_shift=[1,1],**kwargs):
        # XENONnT ALP DM
        dat = loadtxt("limit_data/AxionElectron/XENONnT.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=1,zorder=zorder,lw=lw)

        if text_on:
            plt.text(text_shift[0]*8e2,text_shift[1]*0.82e-14,r'{\bf XENONnT}',fontsize=fs,color=col,ha='center',va='top',clip_on=True)

    def XENONnT_Solar(ax,col='darkred',fs=30,text_on=True,zorder=0.52,lw=2,text_shift=[1,1],**kwargs):
        # Solar axions
        dat = loadtxt("limit_data/AxionElectron/XENONnT_Solar.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=1,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_shift[0]*0.2e-8,text_shift[1]*4e-12,r'{\bf XENONnT (Solar axions)}',fontsize=fs,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
        return

    def SolarBasin(ax,col='#7d203c',fs=20,text_on=True,lw=1.5,text_shift=[0.8,1],zorder=0.6,**kwargs):
        # Solar axion basin arXiv:[2006.12431]
        dat = loadtxt("limit_data/AxionElectron/XENON1T_S2_SolarAxionBasin.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=1,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_shift[0]*3e3,text_shift[1]*2e-11,r'{\bf XENON1T}',fontsize=fs,color='w',ha='center',va='top',clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
            plt.text(text_shift[0]*3e3,text_shift[1]*1.3e-11,r'(Solar axion',fontsize=fs,color='w',ha='center',va='top',clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
            plt.text(text_shift[0]*3e3,text_shift[1]*0.8e-11,r' basin)',fontsize=fs,color='w',ha='center',va='top',clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
        return

    def LUX(ax,col='indianred',fs=30,text_on=True,lw=1.5,text_pos=[0.2e-8,7e-12],zorder=0.52,**kwargs):
        # LUX arXiv:[1704.02297]
        dat = loadtxt("limit_data/AxionElectron/LUX.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=1,zorder=zorder,lw=lw)

        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf LUX (Solar axions)}',fontsize=fs,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
        return

    def PandaX(ax,col='firebrick',fs=20,text_on=True,lw=1.5,text_pos=[1.2e3,4.5e-13],zorder=0.53,rotation=20,**kwargs):
        dat = loadtxt("limit_data/AxionElectron/PandaX.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=1,zorder=zorder,lw=lw)

        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf PandaX}',fontsize=fs-2,color='w',ha='left',va='top',rotation=rotation,clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
        return

    def GERDA(ax,col='#d13617',fs=22,text_on=True,text_pos=[1.6e5,1.9e-11],zorder=0.52,lw=1.5,text_col='w',**kwargs):
        dat = loadtxt("limit_data/AxionElectron/GERDA.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=1,zorder=zorder,lw=lw)

        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf GERDA}',fontsize=fs,color=text_col,ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
        return

    def EDELWEISS(ax,col='#8f2a1f',projection=False,fs=10,text_col='w',text_on=True,text_pos=[1.25e4,1.4e-12],zorder=0.57,lw=1.5,rotation=60,**kwargs):
        # EDELWEISS arXiv:[1808.02340]
        dat = loadtxt("limit_data/AxionElectron/EDELWEISS.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'k-',alpha=1,zorder=zorder,lw=lw)

        if projection:
            dat = loadtxt("limit_data/AxionElectron/Projections/EDELWEISS.txt")
            plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf EDELWEISS',fontsize=fs,rotation=rotation,color=text_col,path_effects=line_background(1.5,'k'),clip_on=True)

        return

    def SuperCDMS(ax,col='#800f24',fs=20,text_on=True,text_pos=[5e1,2.7e-11],text_col='w',zorder=0.58,rotation=-84,lw=1.5,**kwargs):
        # SuperCDMS arXiv:[1911.11905]
        dat = loadtxt("limit_data/AxionElectron/SuperCDMS.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf SuperCDMS}',fontsize=fs-1,color=text_col,ha='left',va='top',alpha=1.0,rotation=rotation,clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
        return

    def DarkSide(ax,col='#921f24',fs=20,text_on=True,text_pos=[4.3e1,1.45e-12],text_col='w',zorder=0.55,rotation=-66,lw=1.5,**kwargs):
        dat = loadtxt("limit_data/AxionElectron/DarkSide.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf DarkSide}',fontsize=fs-1,color=text_col,ha='left',va='top',alpha=1.0,rotation=rotation,clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
        return

    def DARWIN(ax,col='brown',fs=20,text_on=True,text_pos=[0.3e3,2e-14],zorder=0.1,lw=3,**kwargs):
        # DARWIN arXiv:[1606.07001]
        dat = loadtxt("limit_data/AxionElectron/Projections/DARWIN.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf DARWIN}',fontsize=fs,color=col,ha='left',va='top',clip_on=True,**kwargs)
        return

    def LZ(ax,col='crimson',fs=20,text_on=True,text_pos=[2.3e3,0.8e-14],lw=3,zorder=0.1,**kwargs):
        # DARWIN arXiv:[2102.11740]
        dat = loadtxt("limit_data/AxionElectron/Projections/LZ.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf LZ}',fontsize=fs,color=col,ha='left',va='top',clip_on=True,**kwargs)
        return

    def Semiconductors(ax,col='darkred',fs=15,text_on=True,text_pos=[0.9e0,1.7e-12],lw=2,rotation=-80,zorder=0.51,**kwargs):
        # ALP Absorption with semiconductors arXiv:[1608.02123]
        dat = loadtxt("limit_data/AxionElectron/Projections/SemiconductorAbsorption.txt")
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf Semiconductors}',fontsize=fs,color=col,ha='left',va='top',rotation=rotation,clip_on=True,**kwargs)
        return

    def NVCenters(ax,col='red',fs=20,text_on=True,text_shift=[1,1],lw=2,zorder=-0.5,rotation=65,**kwargs):
        # NV center dc magnetometery
        dat = loadtxt("limit_data/AxionElectron/Projections/NVCenters.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,alpha=0.2,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=0.7,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_shift[0]*2.4e-9,text_shift[1]*0.8e-13,r'{\bf NVCenters}',rotation=rotation,alpha=0.7,fontsize=fs-1,color=col,ha='center',va='top',clip_on=True,**kwargs)
        return

    def Magnon(ax,col='crimson',fs=18,text_on=True,text_pos=[1.2e-6,1e-14],lw=2,zorder=0.51,**kwargs):
        # Axion-magnon conversion arXiv:[2005.10256]
        dat = loadtxt("limit_data/AxionElectron/Projections/Magnon.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,alpha=0.2,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=0.7,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf Magnons \newline (YIT, NiSP$_3$)}',fontsize=fs,alpha=0.7,color=col,ha='left',va='top',clip_on=True,**kwargs)
        return

    def MagnonScan(ax,col='darkred',fs=18,text_on=True,text_shift=[1,1],lw=2,zorder=0.5,**kwargs):
        # Axion-magnon conversion arXiv:[2005.10256 and 2001.10666]
        dat = loadtxt("limit_data/AxionElectron/Projections/MagnonScan.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,alpha=0.2,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=0.7,zorder=zorder,lw=lw)
        if text_on:
            plt.text(text_shift[0]*1.3e-5,text_shift[1]*0.5e-13,r'{\bf Magnons}',fontsize=fs-1,alpha=0.7,color=col,ha='center',va='top',clip_on=True,**kwargs)
            plt.text(text_shift[0]*1.3e-5,text_shift[1]*0.7*0.5e-13,r'{\bf (Scanning)}',fontsize=fs-1,alpha=0.7,color=col,ha='center',va='top',clip_on=True,**kwargs)
        return

    def QUAX(ax,col='crimson',fs=17,text_on=True,text_pos=[50e-6,0.9e-10],lw=1,zorder=10.0,text_rot=-90,**kwargs):
        # QUAX https://inspirehep.net/literature/1777123
        dat = loadtxt("limit_data/AxionElectron/QUAX.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,alpha=0.4,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'-',color=col,alpha=1.0,zorder=zorder,lw=lw,path_effects=line_background(lw+2,'k'))
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf QUAX}',fontsize=fs,color=col,rotation=text_rot,ha='left',va='top',clip_on=True,**kwargs)
        return

    def RedGiants(ax,col=[0.0, 0.66, 0.42],text_pos=[0.2e-8,2e-13],text_on=True,zorder=0.5,fs=30,lw=2,**kwargs):
        # Red Giants arXiv:[2007.03694]
        dat = loadtxt("limit_data/AxionElectron/RedGiants_HighMass.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=zorder,lw=lw)
        if text_on: plt.text(text_pos[0],text_pos[1],r'{\bf Red giants (}$\omega${\bf Cen)}',fontsize=fs,color='w',clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
        return

    def Xrays(ax,col='green',text_shift=[1,1],text_on=True,zorder=0.5,fs=17,rotation=-80,alpha=0.3,**kwargs):
        dat = loadtxt("limit_data/AxionElectron/Xray_1loop.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder,alpha=alpha)
        plt.plot(dat[:,0],dat[:,1],':',color='k',zorder=zorder,lw=2,alpha=1)

        if text_on:
            plt.text(1.5e4*text_shift[0],1.17e-15*text_shift[1],r'{\bf X-rays} (EM-anomaly free)',fontsize=fs,color='k',clip_on=True,rotation=rotation,**kwargs)
            #plt.text(1.32e4*text_shift[0],1.2e-15*text_shift[1],r'(EM anomaly-free ALP)',fontsize=fs*0.85,color='w',clip_on=True,rotation=rotation,**kwargs)

            return

    def SolarNu(ax,col='seagreen',text_pos=[0.2e-8,3.8e-11],text_on=True,zorder=0.7,fs=30,lw=2,**kwargs):
        # Solar neutrinos arXiv:[0807.2926]
        dat = loadtxt("limit_data/AxionElectron/SolarNu.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor=None,facecolor=col,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=zorder,lw=lw)
        if text_on: plt.text(text_pos[0],text_pos[1],r'{\bf Solar} $\nu$',fontsize=fs,color='w',clip_on=True,path_effects=line_background(1.5,'k'),**kwargs)
        return

    def WhiteDwarfHint(ax,col='k',text_pos=[1e-7,1e-13],facealpha=0.3,zorder=1.0,text_on=True,fs=20,**kwargs):
        # White dwarf hint arXiv:[1708.02111]
        dat = loadtxt("limit_data/AxionElectron/WDhint.txt")
        plt.fill_between(dat[:,0],dat[:,1],color=col,edgecolor=None,lw=0.001,zorder=zorder,alpha=facealpha)
        if text_on: plt.text(text_pos[0],text_pos[1],r'{\bf White dwarf hint}',fontsize=fs,clip_on=True,**kwargs)
        return

    def StellarBounds(ax,fs=30,Hint=True,text_on=True):
        AxionElectron.RedGiants(ax,text_on=text_on)
        AxionElectron.SolarNu(ax,text_on=text_on)
        if Hint:
            AxionElectron.WhiteDwarfHint(ax,text_on=text_on)
        return

    def IrreducibleFreezeIn(ax,text_label=r'{\bf Freeze-in}',text_pos=[1.9e5,0.7e-14],col='#376631',
                        edgecolor='k',text_col='w',fs=24,zorder=0.009,text_on=True,lw=1,facealpha=1,rotation=-85,edgealpha=1):
        dat = loadtxt("limit_data/AxionElectron/IrreducibleFreezeIn.txt")
        FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,
                    rotation=rotation,edgecolor=edgecolor,fs=fs,
                    zorder=zorder,text_on=text_on,lw=lw,ha='right',facealpha=facealpha,edgealpha=edgealpha,path_effects=line_background(1.5,'k'))
        return

    def UndergroundDetectors(ax,projection=False,fs=20,text_on=True):
        AxionElectron.XENONnT_Solar(ax,fs=fs+10,text_on=text_on)
        AxionElectron.PandaX(ax,fs=fs,text_on=text_on)
        AxionElectron.XENON1T(ax,fs=fs-2,text_on=text_on)
        AxionElectron.XENONnT(ax,fs=fs-2,text_on=text_on)
        AxionElectron.SolarBasin(ax,fs=fs-2,text_on=text_on)
        AxionElectron.SuperCDMS(ax,fs=fs,text_on=text_on)
        AxionElectron.EDELWEISS(ax,fs=fs-5,projection=projection,text_on=text_on)
        AxionElectron.DarkSide(ax,fs,text_on=text_on)
        if projection:
            AxionElectron.DARWIN(ax,fs=fs,text_on=text_on)
            AxionElectron.LZ(ax,fs=fs,text_on=text_on)
            AxionElectron.Semiconductors(ax,fs=fs-5,text_on=text_on)
        return

    def Haloscopes(ax,projection=False,fs=20,text_on=True):
        if projection:
            AxionElectron.Magnon(ax,fs=fs,text_on=text_on)
            AxionElectron.MagnonScan(ax,fs=fs,text_on=text_on)
        return
#==============================================================================#


#==============================================================================#
class AxionNeutron():
    # Warning: often couplings are actually given as g_an/2 m_n (this is what is in the limit_data files)
    # But we are using the dimensionless coupling, so will multiply by the neutron mass
    # this makes essentially no observable difference to the plot but it useful to remember.
    m_n = 0.93957

    def QCDAxion(ax,C_logwidth=10,KSVZ_on=True,DFSZ_on=True,edgecolor='goldenrod',facecolor='gold',alpha=0.04,nlevels=50,fs=25,Mpl_lab=False,DFSZ_label_mass=1e-7,KSVZ_label_mass=1e-6):
        ## QCD Axion band:
        g_min,g_max = ax.get_ylim()
        m_min,m_max = ax.get_xlim()

        # Mass-coupling relation
        def g_x(C_ae,m_a):
            return 1.644e-7*C_ae*m_a
        DFSZ_l = 0.16
        DFSZ_u = 0.26
        KSVZ = 0.02

        if Mpl_lab:
            plt.plot([3.5e-13,3.5e-13],[g_min,g_max],'k--',lw=3)
            plt.text(3.5e-13/4,5e-16,r'$f_a\sim M_{\rm Pl}$',fontsize=fs,rotation=90)

        m_vals = array([1e-10,1e-2])
        g_QCD_upper = 1.644e-7*0.26*m_vals
        for i in flipud(logspace(0,6.5,nlevels)):
            ax.fill_between(m_vals,g_QCD_upper/i,y2=g_QCD_upper,color=facecolor,\
                            alpha=alpha,zorder=-100,lw=3)

        # QCD Axion models
        n = 200
        m = logspace(log10(m_min),log10(m_max),n)
        rot = 45.0
        trans_angle = plt.gca().transData.transform_angles(array((rot,)),array([[0, 0]]))[0]
        if KSVZ_on:
            plt.plot(m,g_x(KSVZ,m),'k-',lw=3.5,zorder=0)
            plt.plot(m,g_x(KSVZ,m),'-',lw=2,zorder=0,color=edgecolor)
            plt.text(KSVZ_label_mass,g_x(KSVZ,KSVZ_label_mass)/2,r'{\bf KSVZ}',fontsize=fs,
            rotation=trans_angle,color=edgecolor,ha='left',va='top',rotation_mode='anchor',clip_on=True,path_effects=line_background(1.5,'k'))

        if DFSZ_on:
            plt.plot(m,g_x(DFSZ_u,m),'k-',lw=3.5,zorder=0)
            plt.plot(m,g_x(DFSZ_u,m),'-',lw=2,zorder=0,color=edgecolor)
            plt.text(DFSZ_label_mass,g_x(DFSZ_l,DFSZ_label_mass)*10,r'{\bf DFSZ models}',fontsize=fs,
            rotation=trans_angle,color=edgecolor,ha='left',va='top',rotation_mode='anchor',clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def OldComagnetometers(ax,col=[0.75, 0.2, 0.2],fs=20,projection=True):
        # Old comagnetometer data arXiv:[1907.03767]
        y2 = ax.get_ylim()[1]
        zo = 0.3
        dat = loadtxt("limit_data/AxionNeutron/OldComagnetometers.txt")
        dat[:,1] *= 2*AxionNeutron.m_n
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=2.5)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=1.0)
        plt.text(2e-20,3e-5,r'{\bf Old comagnetometers}',fontsize=fs,color='w',ha='center',va='top',rotation=-10,clip_on=True,path_effects=line_background(1.5,'k'))
        if projection:
            dat = loadtxt("limit_data/AxionNeutron/Projections/FutureComagnetometers.txt")
            dat[:,1] *= 2*AxionNeutron.m_n
            plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=1,lw=3)
            plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0,alpha=0.5)
            plt.text(5e-18,2*0.5e-12,r'{\bf Future comagnetometers}',fontsize=fs-1,color=col,ha='left',va='top',clip_on=True)
        return

    def nEDM(ax,col=[0.5, 0.0, 0.13],fs=20,projection=True):
        # arXiv:[1902.04644]
        y2 = ax.get_ylim()[1]
        zo = 1
        dat = loadtxt("limit_data/AxionNeutron/nEDM.txt")
        dat[:,1] *= 2*AxionNeutron.m_n
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=3)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.text(0.5e-19,3e-4,r'{\bf nEDM}',fontsize=fs,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))
        return


    def NASDUCK(ax,col=[0.77, 0.1, 0.13],fs=24,projection=True):
        y2 = ax.get_ylim()[1]
        zo = 1
        dat = loadtxt("limit_data/AxionNeutron/NASDUCK.txt")
        dat[:,1] *= 2*AxionNeutron.m_n

        dat2 = loadtxt("limit_data/AxionNeutron/NASDUCK-SERF.txt")
        dat2[:,1] *= 2*AxionNeutron.m_n

        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)

        i1 = 0
        plt.fill_between(dat2[i1:,0],dat2[i1:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat2[i1:,0],dat2[i1:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)
        plt.text(0.7e-13,5e-5,r'{\bf NASDUCK}',fontsize=fs,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def JEDI(ax,text_pos=[3.85e-10,1.1e-6],col='#a3435e',text_col='w',text_rot=90,fs=20,zorder=0.499):
        dat = loadtxt('limit_data/AxionNeutron/JEDI.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=1,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf JEDI}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def PSI_HgM(ax,col='#a82920',fs=21,rotation=40):
        y2 = ax.get_ylim()[1]
        zo = 1.001
        dat = loadtxt("limit_data/AxionNeutron/PSI_HgM.txt")
        dat[:,1] *= 2*AxionNeutron.m_n
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=3)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.text(0.2e-15,1.3e-3,r'{\bf PSI HgM}',rotation=rotation,fontsize=fs,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def SuperfluidHe3(ax,col='darkred',zo=-10):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/AxionNeutron/Projections/SuperfluidHe3.txt")
        dat[:,1] *= 2*AxionNeutron.m_n
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=zo,lw=1.5)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=0.2)
        plt.text(2.8e-8,1e-9,r'{\bf Supefluid $^3$He}',fontsize=16,color=col,ha='left',va='top',clip_on=True,rotation=90)
        return


    class CASPEr():
        def ZULF(ax,col=[0.6, 0.1, 0.1],fs=20,projection=True):
            # arXiv:[1902.04644]
            y2 = ax.get_ylim()[1]
            zo = 2
            dat = loadtxt("limit_data/AxionNeutron/CASPEr_ZULF.txt")
            dat[:,1] *= 2*AxionNeutron.m_n
            plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=1.0)
            plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1.0,zorder=zo,lw=1.5)
            plt.text(3.5e-16,7e-4,r'{\bf CASPEr-ZULF}',fontsize=fs-3,color='w',ha='left',va='top',rotation=40.5,rotation_mode='anchor',clip_on=True,path_effects=line_background(1.5,'k'))
            if projection:
                dat = loadtxt("limit_data/AxionNeutron/Projections/CASPEr_ZULF.txt")
                dat[:,1] *= 2*AxionNeutron.m_n
                plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.0,alpha=0.3)
                plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=0.1,lw=3)
                plt.text(1.3e-22,2*8e-11,r'{\bf CASPEr-ZULF} (projected)',fontsize=fs,color=col,ha='left',va='top',clip_on=True)
            return

        def Comagnetometer(ax,col='darkred',fs=20,projection=True):
            # arXiv:[1901.10843]
            y2 = ax.get_ylim()[1]
            zo = 1.5
            dat = loadtxt("limit_data/AxionNeutron/CASPEr_Comagnetometer.txt")
            dat[:,1] *= 2*AxionNeutron.m_n
            plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=1.0)
            plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=0.8,zorder=zo,lw=1.5)
            plt.text(0.2e-21,8e-3,r'{\bf CASPEr-ZULF (Comag.)}',fontsize=fs-1,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))
            return

        def wind(ax,col='red',fs=20,projection=True):
            # arXiv:[1711.08999]
            y2 = ax.get_ylim()[1]
            zo = -1
            dat = loadtxt("limit_data/AxionNeutron/Projections/CASPEr_wind.txt")
            dat[:,1] *= 2*AxionNeutron.m_n
            plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=0.3)
            plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=1.0,zorder=zo,lw=3)
            plt.text(1.0e-9,0.7e-11,r'{\bf CASPEr}-gradient',fontsize=fs,color=col,ha='left',va='top',rotation=28,clip_on=True)
            return

    def K3He_Comagnetometer_DarkMatter(ax,col='#8a1d34',fs=23,projection=True):
        y2 = ax.get_ylim()[1]
        zo = 0.5
        dat = loadtxt("limit_data/AxionNeutron/K-3He_Comagnetometer_DarkMatter.txt")
        dat[:,1] *= 2*AxionNeutron.m_n
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=1)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)
        plt.text(0.5e-15,8e-9,r'{\bf K-}$^3${\bf He}',fontsize=fs,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def LabExperiments(ax,projection=True,fs=20):
        y2 = ax.get_ylim()[1]

        # Long range spin dependent forces K-3He arXiv:[0809.4700]
        zo = 0.2
        col = 'dimgray'
        dat = loadtxt("limit_data/AxionNeutron/K-3He_Comagnetometer.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)
        plt.text(2.0e-8,3e-4,r'{\bf K-}$^3${\bf He}',fontsize=fs,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))

        # Torsion balance test of gravitational inverse square law: hep-ph/0611184
        # reinterpreted in: hep-ph/0611223
        zo = 0.21
        col = [0.2, 0.25, 0.25]
        #scale = 1.5/4.9 # to convert from pseudoscalar constraint to derivative constraint
        dat = loadtxt("limit_data/AxionNeutron/TorsionBalance.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)
        plt.text(1e-8,2.5e-3,r'{\bf Torsion balance}',fontsize=fs*1.1,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))

        # Casimir effect
        zo = 0.21
        col = [0.2, 0.15, 0.15]
        dat = loadtxt("limit_data/AxionNeutron/Casimir.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)
        plt.text(1e-5,3e-2,r'{\bf Casimir}',fontsize=fs*1.1,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))


        # SNO, axion-induced dissociation of deuterons  arXiv:[2004.02733]
        zo = 0.03
        col = 'darkred'
        dat = loadtxt("limit_data/AxionNeutron/SNO.txt")
        dat[:,1] *= AxionNeutron.m_n # Note that their notation defines their g_an as my g_an/m_n not g_an/2m_n as other use.
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)
        plt.text(0.7e-2,1.6e-4,r'{\bf SNO}',fontsize=fs+6,color='w',ha='right',va='top',clip_on=True,path_effects=line_background(1.5,'k'))
        return
    
    def ElectrostaticStorageRing(ax,col='red',fs=18):
        y2 = ax.get_ylim()[1]
        zo = -1
        dat = loadtxt("limit_data/AxionNeutron/Projections/ElectrostaticStorageRing.txt")
        dat[:,1] *= 2*AxionNeutron.m_n
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=0.1)
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=0.7,zorder=zo,lw=2.3)
        plt.text(0.70e-15,0.7e-12,r'{\bf Electrostatic storage ring}',fontsize=fs,color=col,ha='left',va='top',rotation=43,clip_on=True)
        return


    def Haloscopes(ax,projection=True,fs=20):
        AxionNeutron.OldComagnetometers(ax,projection=projection,fs=fs)
        AxionNeutron.NASDUCK(ax,fs=fs)
        AxionNeutron.CASPEr.ZULF(ax,projection=projection,fs=fs)
        AxionNeutron.CASPEr.Comagnetometer(ax,projection=projection,fs=fs)
        AxionNeutron.nEDM(ax,projection=projection,fs=fs+5)
        AxionNeutron.K3He_Comagnetometer_DarkMatter(ax)
        AxionNeutron.JEDI(ax)
        AxionNeutron.PSI_HgM(ax)

        if projection:
            AxionNeutron.CASPEr.wind(ax,fs=fs)
            AxionNeutron.SuperfluidHe3(ax)
            AxionNeutron.ElectrostaticStorageRing(ax)
        return

    def StellarBounds(ax,fs=24):
        y2 = ax.get_ylim()[1]

        zo = 0.029
        # Stellar physics constraints
        # SN1987A cooling nucleon-nucleon Bremsstrahlung arXiv:[1906.11844]
        # SN = loadtxt("limit_data/AxionNeutron/SN1987A.txt")
        # plt.fill_between(SN[:,0],SN[:,1],y2=y2,edgecolor=None,facecolor='#067034',zorder=zo)
        # plt.plot(SN[:,0],SN[:,1],'k-',alpha=1,lw=2.5,zorder=zo)
        # plt.text(0.8e-2,2.4e-9,r'{\bf SN1987A}',fontsize=fs-7,color='w',ha='right',va='top',clip_on=True,path_effects=line_background(1.5,'k'))

        # https://arxiv.org/pdf/2111.09892.pdf
        SN = loadtxt("limit_data/AxionNeutron/NeutronStars.txt")
        plt.fill_between(SN[:,0],SN[:,1],y2=y2,edgecolor=None,facecolor='DarkGreen',zorder=zo)
        plt.plot(SN[:,0],SN[:,1],'k-',alpha=1,lw=2.5,zorder=zo)
        plt.text(0.8e-2,0.8e-8,r'{\bf Neutron star cooling}',fontsize=fs,color='w',ha='right',va='top',clip_on=True,path_effects=line_background(1.5,'k'))

#==============================================================================#


#==============================================================================#
class AxionProton():
    m_p = 0.93828

    def QCDAxion(ax,C_logwidth=10,KSVZ_on=True,DFSZ_on=True,
                      edgecolor='goldenrod',facecolor='gold',fs=25,Mpl_lab=False,DFSZ_label_mass=1e-6,KSVZ_label_mass=1e-6):
        ## QCD Axion band:
        g_min,g_max = ax.get_ylim()
        m_min,m_max = ax.get_xlim()

        # Mass-coupling relation
        def g_x(C_ae,m_a):
            return 1.64e-7*C_ae*m_a
        DFSZ_l = 0.2
        DFSZ_u = 0.6
        KSVZ = 0.46

        if Mpl_lab:
            plt.plot([3.5e-13,3.5e-13],[g_min,g_max],'k--',lw=3)
            plt.text(3.5e-13/4,5e-16,r'$f_a\sim M_{\rm Pl}$',fontsize=fs,rotation=90)

        # QCD Axion models
        n = 200
        m = logspace(log10(m_min),log10(m_max),n)
        rot = 45.0
        trans_angle = plt.gca().transData.transform_angles(array((rot,)),array([[0, 0]]))[0]
        if KSVZ_on:
            plt.plot(m,g_x(KSVZ,m),'k-',lw=3.5,zorder=0)
            plt.plot(m,g_x(KSVZ,m),'-',lw=2,zorder=0,color=edgecolor)
            plt.text(KSVZ_label_mass,g_x(KSVZ,KSVZ_label_mass)*6,r'{\bf KSVZ}',fontsize=fs,
                rotation=trans_angle,color=edgecolor,ha='left',va='top',rotation_mode='anchor',clip_on=True,path_effects=line_background(1.5,'k'))

        if DFSZ_on:
            plt.fill_between(m,g_x(DFSZ_l,m),y2=g_x(DFSZ_u,m),facecolor=facecolor,zorder=0,alpha=0.5)
            plt.text(DFSZ_label_mass,g_x(DFSZ_l,DFSZ_label_mass)/2,r'{\bf DFSZ models}',fontsize=fs,
                    rotation=trans_angle,color=edgecolor,ha='left',va='top',rotation_mode='anchor',clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def NASDUCK(ax,col=[0.77, 0.1, 0.13],fs=17,projection=True):
        y2 = ax.get_ylim()[1]
        zo = 1
        #dat = loadtxt("limit_data/AxionProton/NASDUCK.txt") # this limit seems to have been retracted so is commented out
        #dat[:,1] *= 2*AxionProton.m_p
        #plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        #plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)

        dat1 = loadtxt("limit_data/AxionProton/NASDUCK-SERF.txt")
        dat1[:,1] *= 2*AxionProton.m_p
        plt.fill_between(dat1[:,0],dat1[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat1[:,0],dat1[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)
        plt.text(1.9e-12,5e-4,r'{\bf NASDUCK}',fontsize=fs,color='w',ha='left',va='top',path_effects=line_background(1.5,'k'))
        return

    def LabExperiments(ax,projection=True,fs=20):
        y2 = ax.get_ylim()[1]

        # Torsion balance test of gravitational inverse square law: hep-ph/0611184
        # reinterpreted in: hep-ph/0611223
        zo = 0.21
        col = [0.2, 0.25, 0.25]
        dat = loadtxt("limit_data/AxionProton/TorsionBalance.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)
        plt.text(1e-8,2e-3,r'{\bf Torsion balance}',fontsize=fs*1.1,color='w',ha='left',va='top',path_effects=line_background(1.5,'k'),clip_on=True)

        # Casimir effect
        zo = 0.21
        col = [0.2, 0.15, 0.15]
        dat = loadtxt("limit_data/AxionProton/Casimir.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)
        plt.text(1e-5,3e-2,r'{\bf Casimir}',fontsize=fs*1.1,color='w',ha='left',va='top',clip_on=True,path_effects=line_background(1.5,'k'))


        # SNO, axion-induced dissociation of deuterons  arXiv:[2004.02733]
        zo = 0.03
        col = 'darkred'
        dat = loadtxt("limit_data/AxionProton/SNO.txt")
        dat[:,1] *= AxionProton.m_p # Note that their notation defines their g_an as my g_an/m_n not g_an/2m_n as other use.
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo)
        plt.plot(dat[:,0],dat[:,1],'-',color='k',alpha=1,zorder=zo,lw=1.5)
        plt.text(0.7e-2,1.6e-4,r'{\bf SNO}',fontsize=fs+6,color='w',ha='right',va='top',path_effects=line_background(1.5,'k'),clip_on=True)
        return
    
    def ProtonStorageRing(ax,col='red',fs=20):
        y2 = ax.get_ylim()[1]
        zo = -1
        dat = loadtxt("limit_data/AxionProton/Projections/ProtonStorageRing.txt")
        dat[:,1] *= 2*AxionProton.m_p
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zo,alpha=0.1)
        plt.plot(dat[:,0],dat[:,1],'--',color=col,alpha=0.7,zorder=zo,lw=2.3)
        plt.text(0.2e-21,0.4e-11,r'{\bf Proton storage ring}',fontsize=fs,color=col,ha='left',va='top',rotation=0,clip_on=True)
        return

    def Haloscopes(ax,projection=True,fs=20):
        AxionProton.NASDUCK(ax)
        AxionNeutron.CASPEr.ZULF(ax,projection=projection,fs=fs)
        AxionNeutron.CASPEr.Comagnetometer(ax,projection=projection,fs=fs)
        if projection:
            AxionNeutron.CASPEr.wind(ax,fs=fs)
            AxionProton.ProtonStorageRing(ax)
        return

    def StellarBounds(ax,fs=30):
        y2 = ax.get_ylim()[1]

        # Stellar physics constraints
        # SN1987A cooling nucleon-nucleon Bremsstrahlung arXiv:[1906.11844]
        # SN = loadtxt("limit_data/AxionProton/SN1987A.txt")
        # plt.fill_between(SN[:,0],SN[:,1],y2=y2,edgecolor=None,facecolor='#067034',zorder=0.01)
        # plt.plot(SN[:,0],SN[:,1],'k-',alpha=1,lw=2.5,zorder=0.01)
        # plt.text(0.8e-2,1.3e-5,r'{\bf SN1987A}',fontsize=fs,color='w',ha='right',va='top',path_effects=line_background(1.5,'k'),clip_on=True)

        # NS cooling Buschmann et al.
        SN = loadtxt("limit_data/AxionProton/NeutronStars.txt")
        plt.fill_between(SN[:,0],SN[:,1],y2=y2,edgecolor=None,facecolor='DarkGreen',zorder=0.02)
        plt.plot(SN[:,0],SN[:,1],'k-',alpha=1,lw=2.5,zorder=0.02)
        plt.text(0.8e-2,0.8e-8,r'{\bf Neutron star cooling}',fontsize=fs-6,color='w',ha='right',va='top',path_effects=line_background(1.5,'k'),clip_on=True)
#==============================================================================#


#==============================================================================#
class AxionEDM():
    def QCDAxion(ax,shading_on=True,C_logwidth=10,C_width=0.4,
                      cmap='YlOrBr',fs=28,QCD_label_mass=1e-6,\
                 text_on=True,text_col='gold',alpha=0.5,rot=45.0,zorder=-100):
        ## QCD Axion band:
        g_min,g_max = ax.get_ylim()
        m_min,m_max = ax.get_xlim()

        # Mass-coupling relation
        def g_x(C,m_a):
            return 6.4e-10*C*m_a


        if shading_on:
            n = 200
            g = logspace(log10(g_min),log10(g_max),n)
            m = logspace(log10(m_min),log10(m_max),n)
            QCD = zeros(shape=(n,n))
            for i in range(0,n):
                QCD[:,i] = norm.pdf(log10(g)-log10(g_x(1,m[i])),0.0,C_width)
            cols = cm.get_cmap(cmap)

            cols.set_under('w') # Set lowest color to white
            vmin = amax(QCD)/(C_logwidth/8)
            plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=1.3,zorder=zorder)
            plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=1.3,zorder=zorder)
            plt.contourf(m, g, QCD, 50,cmap=cols,vmin=vmin,vmax=1.3,zorder=zorder)
        else:
            n = 200
            col ='goldenrod'
            m = logspace(log10(m_min),log10(m_max),n)
            plt.fill_between(m,g_x(1-0.4,m),y2=g_x(1+0.4,m),facecolor=col,zorder=0,alpha=alpha)

        if text_on:
            trans_angle = plt.gca().transData.transform_angles(array((rot,)),array([[0, 0]]))[0]
            plt.text(QCD_label_mass,g_x(1-0.4,QCD_label_mass)/1.4,r'{\bf QCD axion}',\
             fontsize=fs,rotation=trans_angle+1,color=text_col,ha='left',va='top',rotation_mode='anchor',clip_on=True,
             path_effects=line_background(1.4,'k'))
        return

    def nEDM(ax,text_pos=[3e-20,5e-18],col='darkred',text_col='w',text_rot=0,fs=30,zorder=-1,lw=1.5):
        dat = loadtxt('limit_data/AxionEDM/nEDM.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf nEDM}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def BeamEDM(ax,text_pos=[6e-18,2e-15],col='#822f2b',text_col='w',text_rot=32,fs=22,zorder=-1,lw=1.5):
        dat = loadtxt('limit_data/AxionEDM/BeamEDM.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf Beam EDM}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def HfF(ax,text_pos=[0.7e-19,1.5e-14],col='#a3435e',text_col='w',text_rot=33,fs=22,zorder=-1,lw=1.5):
        dat = loadtxt('limit_data/AxionEDM/HfF.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf HfF}$^+$',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def RbQuartz(ax,text_label=r'{\bf Rb/Quartz}',text_pos=[0.15e-16,2e-12],text_rot=28,col='#c11a4e',text_col='w',fs=20,zorder=0.10999,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/AxionEDM/RbQuartz.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=text_rot,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def SN1987A(ax,text_pos=[2e-10,1.2e-8],col='#067034',text_col='w',text_rot=0,fs=33,zorder=1,lw=1.5):
        dat = loadtxt('limit_data/AxionEDM/SN1987A.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf SN1987A}',color=text_col,rotation=text_rot,fontsize=fs,ha='right',clip_on=True,path_effects=line_background(1.5,'k'))
        return


    def PlanckBAO(ax,text_pos=[3e-10,0.5e-9],col='#136919',text_col='w',text_rot=0,fs=26,zorder=0.8,lw=1.5):
        dat = loadtxt('limit_data/AxionEDM/PlanckBAO.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf Planck+BAO}',color=text_col,rotation=text_rot,fontsize=fs,ha='right',clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def BBN(ax,text_pos=[3e-16,4e-18],col='#1f4969',text_col='w',text_rot=33.5,fs=23,zorder=-6,lw=1.5):
        dat = loadtxt('limit_data/AxionEDM/BBN.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf BBN (dark matter)}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return


    def CASPEr(ax,text_pos=[0.5e-5,0.25e-3],col='crimson',text_col='w',fs=20,zorder=30,projection=False,text_on=True,lw=4):
        dat = loadtxt('limit_data/AxionEDM/CASPEr-electric.txt')
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw+2,alpha=1,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],color=col,lw=lw,alpha=1,zorder=zorder)
        if text_on:
            plt.text(text_pos[0],text_pos[1],r'{\bf CASPEr-electric}',color=text_col,fontsize=fs,ha='right',zorder=zorder,path_effects=line_background(1.5,'k'))
        if projection:
            # dat = loadtxt('limit_data/AxionEDM/Projections/CASPEr-electric-PhaseI.txt')
            # plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,lw=lw-1,alpha=0.05,zorder=-10)
            # plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=-10,lw=lw-1)

            dat = loadtxt('limit_data/AxionEDM/Projections/CASPEr-electric-PhaseII.txt')
            plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,lw=4,alpha=0.05,zorder=-10)
            plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=-10,lw=lw-1)

            dat = loadtxt('limit_data/AxionEDM/Projections/CASPEr-electric-PhaseIII.txt')
            plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,lw=lw-1,alpha=0.05,zorder=-10)
            plt.plot(dat[:,0],dat[:,1],'--',color=col,zorder=-10,lw=lw-1)

            if text_on:
                plt.text(0.4e-11,0.2e-19,r'{\bf CASPEr-electric}',rotation=43,fontsize=25,color=col,clip_on=True)
                #plt.text(0.7e-10,0.08e-11,'phase I',rotation=40,fontsize=20,color=col,clip_on=True)
                plt.text(1.5e-8,3e-15,'phase II',rotation=51.5,fontsize=20,color=col,clip_on=True)
                plt.text(7e-8,0.3e-15,'phase III',rotation=52,fontsize=20,color=col,clip_on=True)
        return

    def JEDI(ax,text_pos=[1.4e-10,1.5e-5],col='#a3435e',text_col='w',text_rot=90,fs=22,zorder=10,lw=1):
        dat = loadtxt('limit_data/AxionEDM/JEDI.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf JEDI}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return



#==============================================================================#


#==============================================================================#
class Axion_fa():
    def QCDAxion(ax,shading_on=True,C_logwidth=10,C_width=0.4,
                      linecolor='gold',fs=28,QCD_label_mass=1e-7,\
                 text_on=True,text_col='gold',alpha=0.5,rot=45.0,zorder=-100):
        ## QCD Axion band:
        g_min,g_max = ax.get_ylim()
        m_min,m_max = ax.get_xlim()

        # Mass-coupling relation
        def f_a(C,m_a):
            return C*(1/1e12)*(m_a/5.7e-6)
        plt.plot([m_min,m_max],[f_a(1,m_min),f_a(1,m_max)],'-',lw=5,path_effects=line_background(6,'k'),color=linecolor,zorder=zorder)

        if text_on:
            trans_angle = plt.gca().transData.transform_angles(array((rot,)),array([[0, 0]]))[0]
            plt.text(QCD_label_mass,f_a(1-0.4,QCD_label_mass)/1.4,r'{\bf QCD axion}',\
                 fontsize=fs,rotation=trans_angle+1,color=text_col,ha='left',va='top',rotation_mode='anchor',clip_on=True,
                 path_effects=line_background(1.4,'k'))
        return

    def nEDM(ax,text_pos=[20e-20,0.3e-14],col='darkred',text_col='w',text_rot=40,fs=23,zorder=-1.1):
        # Already accounts for stochastic correction
        dat = loadtxt('limit_data/fa/nEDM.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=3,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf nEDM}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def BeamEDM(ax,text_pos=[6e-18,6e-13],col='#822f2b',text_col='w',text_rot=40,fs=22,zorder=-1):
        dat = loadtxt('limit_data/fa/BeamEDM.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=1.5,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf Beam EDM}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def HfF(ax,text_pos=[0.7e-19,4e-12],col='#a3435e',text_col='w',text_rot=40,fs=22,zorder=-1):
        dat = loadtxt('limit_data/fa/HfF.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=1.5,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf HfF}$^+$',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def RbQuartz(ax,text_label=r'{\bf Rb/Quartz}',text_pos=[0.15e-16,0.5e-9],text_rot=35,col='#c11a4e',text_col='w',fs=20,zorder=0.10999,text_on=True,Projection=False,edgealpha=1,lw=1.5):
        dat = loadtxt("limit_data/fa/RbQuartz.txt")
        FilledLimit(ax,dat,text_label,y2=1e20,rotation=text_rot,text_pos=text_pos,text_col=text_col,col=col,fs=fs,zorder=zorder,text_on=text_on,edgealpha=edgealpha,lw=lw,path_effects=line_background(1.5,'k'))
        return

    def SolarCore(ax,text_pos=[0.08e-10,0.12e-10],col='#50946e',text_col='w',text_rot=41,fs=30,zorder=-5,lw=2):
        dat = loadtxt('limit_data/fa/SolarCore.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf Solar core}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def WhiteDwarfs(ax,text_pos=[0.9e-10,0.03e-11],col='#599967',text_col='w',text_rot=41,fs=28,zorder=-10,lw=2):
        dat = loadtxt('limit_data/fa/WhiteDwarfs.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf White dwarfs}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def GW170817(ax,text_pos=[7e-16,2e-17],zo=-7,linespacing_y=0.65,col='#95bd93',text_col='k',text_rot=0,fs=23):
        dat = loadtxt('limit_data/fa/GW170817.txt')
        plt.fill_between(dat[:,0],dat[:,1],color=col,zorder=zo,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=3,alpha=1,zorder=zo)
        plt.text(text_pos[0],text_pos[1],r'{\bf GW170817}',color=text_col,rotation=text_rot,fontsize=fs,ha='center',clip_on=True)
        return


    def Pulsars(ax,text_pos=[3e-15,0.11e-16],linespacing_y=0.65,col='#30693d',text_col='#30693d',text_rot=0,fs=21,zo=-6.9):
        dat = loadtxt('limit_data/fa/Pulsar.txt')
        plt.fill_between(dat[:,0],dat[:,1],color=col,zorder=zo,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=3,alpha=1,zorder=zo)
        plt.text(text_pos[0],text_pos[1]*(1-linespacing_y),r'{\bf Pulsars}',color=text_col,rotation=text_rot,fontsize=fs,ha='center',clip_on=True)
        return

    def PlanckBAO(ax,text_pos=[8e-3,1.5e-7],col='#136919',text_col='w',text_rot=0,fs=27,zorder=0.8,lw=1.5):
        dat = loadtxt('limit_data/fa/PlanckBAO.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf Planck+BAO}',color=text_col,rotation=text_rot,fontsize=fs,ha='right',clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def BBN(ax,text_pos=[1.9e-17,0.95e-16],col='#1f4969',text_col='w',text_rot=15,fs=14,zorder=-6):
        dat = loadtxt('limit_data/fa/BBN.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=3,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf BBN}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def SN1987A(ax,text_pos=[7e-3,0.4e-5],col='#067034',text_col='w',text_rot=0,fs=33,zorder=1,lw=2):
        dat = loadtxt('limit_data/fa/SN1987A.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=lw,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf SN1987A}',color=text_col,rotation=text_rot,fontsize=fs,ha='right',clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def NeutronStars(ax,text_pos=[0.5e-3,0.4e-12],col='#599967',text_col='#599967',text_rot=41,fs=29,zorder=-10):
        dat = loadtxt('limit_data/fa/Projections/NeutronStars.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=0.1)
        plt.plot(dat[:,0],dat[:,1],'--',color=col,lw=3,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf Neutron stars}',color=text_col,rotation=text_rot,fontsize=fs,ha='right',clip_on=True)
        return

    def Axinovae(ax,text_pos=[1.7e-20,0.02e-13],col='navy',text_col='w',text_rot=44,fs=20,zorder=-1.01):
        dat = loadtxt('limit_data/fa/Axinovae.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,zorder=zorder,alpha=1)
        plt.plot(dat[:,0],dat[:,1],color='k',lw=3,alpha=1,zorder=zorder)
        plt.text(text_pos[0],text_pos[1],r'{\bf Axinovae}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True,path_effects=line_background(1.5,'k'))
        return

    def Inspirals(ax,text_pos=[1e-16,2e-14],col='darkgreen',text_col='darkgreen',text_rot=0,fs=23,zorder=-10):
        dat = loadtxt('limit_data/fa/Projections/NSBH-Inspiral.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e-99,color=col,zorder=zorder,alpha=0.2)
        plt.plot(dat[:,0],dat[:,1],'--',color=col,lw=3,alpha=1,zorder=zorder)

        dat = loadtxt('limit_data/fa/Projections/NSNS-Inspiral.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e-99,color=col,zorder=zorder,alpha=0.2)
        plt.plot(dat[:,0],dat[:,1],'--',color=col,lw=3,alpha=1,zorder=zorder)

        plt.text(text_pos[0],text_pos[1],r'{\bf Inspirals}',color=text_col,rotation=text_rot,fontsize=fs,clip_on=True)
        return

    def StorageRingEDM(ax,text_pos=[1e-11,1.5e-13],col='crimson',alpha=0.4,zorder=-10,text_rot=41,fs=20):
        dat = loadtxt('limit_data/fa/Projections/StorageRingEDM.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,alpha=0.1,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'--',lw=3,color=col,zorder=zorder,alpha=0.4)
        plt.text(text_pos[0],text_pos[1],r'{\bf Storage ring}',color=col,alpha=0.4,fontsize=fs,rotation=text_rot,clip_on=True)
        return

    def CASPEr(ax,text_pos=[5e-11,1e-19],col='crimson',alpha=0.1,zorder=-10,text_rot=57,fs=23):
        dat = loadtxt('limit_data/fa/Projections/CASPEr-electric-PhaseIII.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,alpha=alpha,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'--',lw=3,color=col,zorder=-1,alpha=1)
        plt.text(text_pos[0],text_pos[1],r'{\bf CASPEr-electric}',color=col,alpha=1,fontsize=fs,rotation=text_rot,clip_on=True)
        return

    def PiezoaxionicEffect(ax,text_pos=[7.6e-10,0.15e-14],col='darkred',alpha=0.4,zorder=-20,text_rot=90,fs=19):
        dat = loadtxt('limit_data/fa/Projections/PiezoaxionicEffect1.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,alpha=0.1,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'--',lw=1.5,color=col,zorder=zorder,alpha=0.4)
        dat = loadtxt('limit_data/fa/Projections/PiezoaxionicEffect64.txt')
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,color=col,alpha=0.1,zorder=zorder)
        plt.plot(dat[:,0],dat[:,1],'--',lw=1.5,color=col,zorder=zorder,alpha=0.4)
        plt.text(text_pos[0],text_pos[1],r'{\bf Piezoaxionic}',color=col,alpha=0.6,fontsize=fs,rotation=text_rot,clip_on=True)
        return
#==============================================================================#


class DarkPhoton():
    def FigSetup(xlab=r'Dark photon mass [eV]',ylab='Kinetic mixing',\
             chi_min = 1.0e-18,chi_max = 1.0e0,\
             m_min = 3e-18,m_max = 1e5,\
             lw=2.5,lfs=40,tfs=25,tickdir='out',\
             Grid=False,Shape='Rectangular',mathpazo=True,\
             TopAndRightTicks=False,FrequencyAxis=True,FrequencyLabels=True,UnitAxis=True,f_rescale=1,\
            tick_rotation = 20,width=20,height=10,upper_tickdir='out'):

        plt.rcParams['axes.linewidth'] = lw
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif',size=tfs)

        if mathpazo:
            plt.rcParams.update({"text.usetex": True,"font.family": "serif","font.serif": ["Palatino"],})


        if Shape=='Wide':
            fig = plt.figure(figsize=(16.5,5))
        elif Shape=='Rectangular':
            fig = plt.figure(figsize=(16.5,11))
        elif Shape=='Custom':
            fig = plt.figure(figsize=(width,height))

        ax = fig.add_subplot(111)

        ax.set_xlabel(xlab,fontsize=lfs)
        ax.set_ylabel(ylab,fontsize=lfs)

        ax.tick_params(which='major',direction=tickdir,width=2.5,length=13,right=TopAndRightTicks,top=TopAndRightTicks,pad=7)
        ax.tick_params(which='minor',direction=tickdir,width=1,length=10,right=TopAndRightTicks,top=TopAndRightTicks)


        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.set_xlim([m_min,m_max])
        ax.set_ylim([chi_min,chi_max])

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
            plt.xticks(rotation=tick_rotation)

        if Grid:
            ax.grid(zorder=0)

        if FrequencyAxis:
            ax2 = ax.twiny()



            ax2.set_xscale('log')
            ax2.tick_params(which='major',direction=upper_tickdir,width=2.5,length=13,pad=7)
            ax2.tick_params(which='minor',direction=upper_tickdir,width=1,length=10)
            locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=50)
            locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10)*.1,numticks=100)
            ax2.xaxis.set_major_locator(locmaj)
            ax2.xaxis.set_minor_locator(locmin)
            ax2.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())

            if FrequencyLabels:
                ax2.set_xticks([1e-3,1e0,1e3,1e6,1e9,1e12,1*241.8*1e12,1000*241.8*1e12])
                ax2.set_xticklabels(['mHz','Hz','kHz','MHz','GHz','THz','eV','keV'])
            ax2.set_xlim([m_min*241.8*1e12/f_rescale,m_max*241.8*1e12/f_rescale])

            plt.sca(ax)
        return fig,ax


    def Haloscopes(ax,fs=17,projection=True,text_on=True,col='darkred'):
        y2 = ax.get_ylim()[1]
        zo = 0.3

        # ADMX
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/ADMX.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1,lw=3)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/ADMX2018.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/ADMX2019_1.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/ADMX2019_2.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/ADMX2021.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/ADMX_Sidecar.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)

        # HAYSTAC
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/HAYSTAC.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/HAYSTAC_2020.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/HAYSTAC_2022.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)

        # CAPP
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/CAPP-1.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/CAPP-2.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/CAPP-3.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/CAPP-4.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/CAPP-5.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/CAPP-6.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)
        dat = loadtxt("limit_data/DarkPhoton/Rescaled/CAST-CAPP.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)

        dat = loadtxt("limit_data/DarkPhoton/Rescaled/TASEH.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.1)

        dat = loadtxt("limit_data/DarkPhoton/Rescaled/ORGAN-1a.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,facecolor=col,zorder=0.21)

        dat = loadtxt("limit_data/DarkPhoton/Rescaled/QUAX.txt")
        dat[0,1] = 1e0
        plt.plot(dat[:,0],dat[:,1],zorder=0.2,color=col,lw=2)

        dat = loadtxt("limit_data/DarkPhoton/Rescaled/QUAX2.txt")
        dat[0,1] = 1e0
        plt.plot(dat[:,0],dat[:,1],zorder=0.2,color=col,lw=2)

        dat = loadtxt("limit_data/DarkPhoton/Rescaled/QUAX3.txt")
        dat[0,1] = 1e0
        plt.plot(dat[:,0],dat[:,1],zorder=0.2,color=col,lw=2)

        if text_on:
            plt.text(1.4e-6,0.5e-14,r'{\bf ADMX}',fontsize=fs,color=ADMX_col,rotation=90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.text(0.8e-5,0.1e-13,r'{\bf CAPP}',fontsize=fs-2,color=CAPP_col,rotation=90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.text(0.19e-4,3e-15,r'{\bf HAYSTAC}',fontsize=fs-5,color=HAYSTAC_col,rotation=90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.text(0.47e-4,3e-12,r'{\bf QUAX}',fontsize=fs-8,color=QUAX_col,rotation=-90,rotation_mode='anchor',ha='center',va='center',clip_on=True)

        return


    def StellarBounds(ax,fs=19,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        # Stellar physics constraints

        # Globular clusters
        HB_col = [0.01, 0.75, 0.24]
        HB = loadtxt("limit_data/DarkPhoton/RG.txt")
        plt.fill_between(HB[:,0],HB[:,1],y2=y2,edgecolor=None,facecolor=HB_col,zorder=0.9)
        plt.plot(HB[:,0],HB[:,1],color='k',alpha=1,zorder=0.9,lw=lw)

        # Globular clusters
        HB_col = 'DarkGreen'
        HB = loadtxt("limit_data/DarkPhoton/HB.txt")
        plt.fill_between(HB[:,0],HB[:,1],y2=y2,edgecolor=None,facecolor=HB_col,zorder=0.95)
        plt.plot(HB[:,0],HB[:,1],color='k',alpha=1,zorder=0.95,lw=lw)

        # Solar bound
        Solar_col = 'ForestGreen'
        Solar = loadtxt("limit_data/DarkPhoton/Solar.txt")
        plt.fill_between(Solar[:,0],Solar[:,1],y2=y2,edgecolor=None,facecolor=Solar_col,zorder=1.02)
        plt.plot(Solar[:,0],Solar[:,1],color='k',alpha=1,zorder=1.02,lw=lw)

        Solar = loadtxt("limit_data/DarkPhoton/Solar-Global.txt")
        plt.fill_between(Solar[:,0],Solar[:,1]/Solar[:,0],y2=y2,edgecolor=None,facecolor=Solar_col,zorder=1.021)
        plt.plot(Solar[:,0],Solar[:,1]/Solar[:,0],color='k',alpha=1,zorder=1.021,lw=lw)

        if text_on:
            plt.text(0.9e2,2.0e-14,r'{\bf Solar}',fontsize=fs,color='w',rotation=-44,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(1e3,2.3e-14,r'{\bf HB}',fontsize=fs,color='w',rotation=-35,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(1e4,0.58e-14,r'{\bf RG}',fontsize=fs,color='w',rotation=-38,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
        return


    def Xenon(ax,col='crimson',fs=23,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/Xenon1T.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)

        plt.fill_between(1e3*dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.5)
        plt.plot(1e3*dat[:,0],dat[:,1],color='k',alpha=1,zorder=0.5,lw=lw)

        dat = loadtxt("limit_data/DarkPhoton/Xenon1T_S1S2.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)

        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.5)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=0.5,lw=lw)


        dat = loadtxt("limit_data/DarkPhoton/XENON1T_SE.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.5)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=0.5,lw=lw)


        dat = loadtxt("limit_data/DarkPhoton/XENON1T_Solar_SE.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=0.0,lw=lw)


        dat = loadtxt("limit_data/DarkPhoton/XENONnT.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.5)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=0.5,lw=lw)

        if text_on:
            plt.text(1.5e3,2.5e-17,r'{\bf XENON}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.text(0.65e-3,2.4e-11,r'{\bf XENON1T}',color='w',rotation=-41,fontsize=15,path_effects=line_background(1,'k'),clip_on=True)


        return





    def DAMIC(ax,col='salmon',fs=21,text_on=True,lw=1.5):
        m1,y1 = loadtxt("limit_data/DarkPhoton/DM_combined.txt",unpack=True)
        dat = loadtxt("limit_data/DarkPhoton/DAMIC.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)

        y2 = interp(dat[:,0],m1,y1)
        dat[0,1] = y2[0]
        dat[-1,1] = y2[-1]
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.001)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.001,lw=lw)

        if text_on:
            plt.text(4e-1,1.3e-14,r'{\bf DAMIC}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.plot([4e0,1e1],[3e-14,6e-14],'-',lw=2.5,color=col,path_effects=line_background(3.5,'k'))
        return

    def MuDHI(ax,col='#400927',fs=15,text_on=True,lw=1.5):
        m1,y1 = loadtxt("limit_data/DarkPhoton/DM_combined.txt",unpack=True)
        dat = loadtxt("limit_data/DarkPhoton/MuDHI.txt")

        y2 = interp(dat[:,0],m1,y1)
        dat[dat[:,1]>y2,1] = y2[dat[:,1]>y2]
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=10)
        plt.plot(dat[::2,0],dat[::2,1],color='k',alpha=1,zorder=10,lw=lw)

        if text_on:
            plt.text(0.18e-2,1e-11,r'{\bf MuDHI}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.plot([1.2e-2,1.5e0],[1e-11,4e-11],'-',lw=2.5,color=col,path_effects=line_background(3.5,'k'))
        return


    def FUNK(ax,col='red',fs=21,text_on=True,lw=1.5):
        m1,y1 = loadtxt("limit_data/DarkPhoton/DM_combined.txt",unpack=True)
        dat = loadtxt("limit_data/DarkPhoton/FUNK.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)*sqrt(2/3/0.27)

        y2 = interp(dat[:,0],m1,y1)
        #dat[0,1] = y2[0]
        dat[dat[:,1]>y2,1] = y2[dat[:,1]>y2]
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.3)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.3,lw=lw)

        if text_on:
            plt.text(1.9e-1,0.8e-13,r'{\bf FUNK}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.plot([7e-1,3e0],[2.5e-13,1e-12],'-',lw=2.5,color=col,path_effects=line_background(3.5,'k'))
        return

    def SENSEI(ax,col='firebrick',fs=21,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/SENSEI.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)

        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1,lw=lw)

        if text_on:
            plt.text(1.7e0,1e-15,r'{\bf SENSEI}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.plot([7e0,1e1],[3e-15,9e-15],'-',lw=2.5,color=col,path_effects=line_background(3.5,'k'))
        return

    def DarkSide(ax,col='#f72a38',fs=18,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/DarkSide.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.1)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=0.5,lw=lw,zorder=0.1)

        if text_on:
            plt.text(0.5e1,0.5e-16,r'{\bf DarkSide}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
        return

    def SuperCDMS(ax,col=[0.4,0,0],fs=18,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/SuperCDMS.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.6)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=0.5,zorder=0.6,lw=lw)

        if text_on:
            plt.text(0.4e0,2.5e-16,r'{\bf SuperCDMS}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.plot([1e1,0.8e2],[3e-16,9e-16],'-',lw=2.5,color=col,path_effects=line_background(3.5,'k'))
        return
    
    def Nanowire(ax,col='pink',fs=22,text_on=True,lw=1.5):
        m1,y1 = loadtxt("limit_data/DarkPhoton/DM_combined.txt",unpack=True)
        dat = loadtxt("limit_data/DarkPhoton/WSi_Nanowire.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)
        y2 = interp(dat[:,0],m1,y1)
        dat[0,1] = y2[0]/1.1
        dat[-1,1] = y2[-1]/1.1
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.3)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.3,lw=lw)

        if text_on:
            plt.text(5e-4,1e-10,r'{\bf WSi Nanowire}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.plot([9e-3,3e-3],[3e-10,9e-10],'-',lw=2.5,color=col)
        return


    def SQMS(ax,col='#02734b',fs=17,text_on=True,lw=0.5,ms=10):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/SQMS.txt")
        dat[:,1] = dat[:,1]*sqrt(1/3/0.019)
        plt.plot(dat[:,0],dat[:,1],lw=lw,color=col,alpha=1,zorder=0.0)
        if text_on:
            plt.text(5.7e-6,0.65e-14,r'{\bf SQMS}',fontsize=fs,color=col,rotation=-90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
        return

    def LAMPOST(ax,col='#471710',fs=15,text_on=True,lw=1.5):
        m1,y1 = loadtxt("limit_data/DarkPhoton/DM_combined.txt",unpack=True)
        dat = loadtxt("limit_data/DarkPhoton/LAMPOST.txt")
        dat[:,1] = dat[:,1]*sqrt(0.4/0.45)*sqrt(2/3/0.27)

        y2 = interp(dat[:,0],m1,y1)
        dat[0,1] = y2[0]/1.1
        dat[-1,1] = y2[-1]/1.1
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0)
        plt.plot(dat[:,0],dat[:,1],color=col,alpha=1,zorder=0,lw=lw)

        if text_on:
            plt.text(0.3e-1,4.5e-13,r'{\bf LAMPOST}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.plot([3e-1,0.6e0],[6e-13,1e-12],'-',lw=1.5,color=col,path_effects=line_background(2,'k'))
        return

    def Tokyo(ax,col='darkred',fs=15,text_on=True,lw=1.5):
        m1,y1 = loadtxt("limit_data/DarkPhoton/DM_combined.txt",unpack=True)
        dat = loadtxt("limit_data/DarkPhoton/Tokyo-Dish.txt")
        dat[:,1] = dat[:,1]*sqrt(2/3/0.6)
        y2 = interp(dat[:,0],m1,y1)
        dat[0,1] = y2[0]
        dat[-1,1] = y2[-1]
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.4)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.4,lw=lw)


        dat = loadtxt("limit_data/DarkPhoton/Tokyo-Knirck.txt")
        dat[:,1] = dat[:,1]*sqrt(1/3/0.175)
        plt.fill_between(dat[:,0],dat[:,1],y2=1e0,edgecolor='k',facecolor=col,zorder=1.09)

        dat = loadtxt("limit_data/DarkPhoton/Tokyo-Tomita.txt")
        plt.plot([dat[1,0],dat[1,0]],[dat[1,1],1e0],'-',color=col,lw=3,zorder=0.2)
        if text_on:
            #plt.text(2e-4,1e-10,r'{\bf Tokyo-3}',fontsize=fs,color=col,rotation=-90,rotation_mode='anchor',ha='center',va='center')
            plt.text(0.45e-3,3e-8,r'{\bf Tokyo-2}',fontsize=fs-2,color='k',rotation=90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.text(0.03e-1,2e-12,r'{\bf Tokyo-1}',fontsize=fs+4,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.plot([0.3e-1,3e0],[2e-12,8e-12],'-',lw=2.5,color=col,path_effects=line_background(3.5,'k'))
        return

    def FAST(ax,col='tomato',fs=10,text_on=True,lw=1.5,edge_on=False,zorder=0.11):
        m1,y1 = loadtxt("limit_data/DarkPhoton/DM_combined.txt",unpack=True)
        dat = loadtxt("limit_data/DarkPhoton/FAST.txt")
        dat[:,1] = dat[:,1]*sqrt(2/3/0.6)
        y2 = interp(dat[:,0],m1,y1)
        dat[0,1] = y2[0]/1.1
        dat[-1,1] = y2[-1]/1.1
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zorder)
        if edge_on:
            plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=zorder,lw=lw)

        if text_on:
            plt.text(7e-6,4e-12,r'{\bf FAST}',fontsize=fs,color=col,rotation=-90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
        return

    def LOFAR(ax,col='red',fs=10,text_on=True,lw=1.5,edge_on=False,zorder=0.11):
        # Solar corona bound
        m1,y1 = loadtxt("limit_data/DarkPhoton/DM_combined.txt",unpack=True)
        dat = loadtxt("limit_data/DarkPhoton/LOFAR.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)
        y2 = interp(dat[:,0],m1,y1)
        dat[0,1] = y2[0]/1.1
        dat[-1,1] = y2[-1]/1.1
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=zorder)
        if edge_on:
            plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=zorder,lw=lw)

        if text_on:
            plt.text(1.95e-7,3e-14,r'{\bf LOFAR (Sun)}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
        return

    def Jupiter(ax,col='Green',fs=15,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/Jupiter.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=2)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=2,lw=lw)
        if text_on:
            plt.text(0.1e-14,4.5e-1,r'{\bf Jupiter}',fontsize=fs,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1,'k'),clip_on=True)
        return

    def Earth(ax,col='DarkGreen',fs=17,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/Earth.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.9)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.9,lw=lw)
        if text_on:
            plt.text(0.4e-13,2e-1,r'{\bf Earth}',fontsize=fs,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1,'k'),clip_on=True)
        return


    def Crab(ax,col=[0.1,0.4,0.1],fs=17,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/Crab.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=2)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=2,lw=lw)

    #     dat = loadtxt("limit_data/DarkPhoton/Crab_2.txt")
    #     plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.9,lw=lw)
    #     plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.9)
        if text_on:
            plt.text(0.5e-6,3e-1,r'{\bf Crab}',fontsize=fs,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1,'k'),clip_on=True)
            plt.text(0.8e-6,0.9e-1,r'{\bf nebula}',fontsize=fs,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1,'k'),clip_on=True)

        return


    def QUALIPHIDE(ax,col='r',fs=9,text_on=True,edge_on=False,lw=0.8,zorder=0):
        # data file is for randomly polarised case and 0.3 GeV/cm^3
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/QUALIPHIDE.txt")
        dat[:,1] = dat[:,1]*sqrt(1/3/0.13)*sqrt(0.3/0.45)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor='k',facecolor=col,zorder=zorder,lw=0)
        if edge_on:
            plt.plot(dat[:,0],dat[:,1],'k-',lw=lw,zorder=zorder)
        if text_on:
            plt.text(3.5e-5,0.13e-12,r'{\bf QUALIPHIDE}',fontsize=fs,color=col,rotation=-90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
        return
        
    def SHUKET(ax,col='maroon',fs=13,text_on=False,edge_on=False,lw=0.8):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/SHUKET.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)*sqrt(1/3/0.038)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.2)
        if edge_on:
            plt.plot(dat[:,0],dat[:,1],'k-',lw=lw,zorder=0.2)
        if text_on:
            plt.text(3.5e-5,0.13e-12,r'{\bf SHUKET}',fontsize=fs,color=col,rotation=-90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
        return

    def DarkEfield(ax,col='darkred',fs=17,text_on=True,edge_on=False,lw=0.8):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/DarkEfield.txt")
        dat[:,1] = dat[:,1]*sqrt(1.64/5) # convert from 5 sigma CL to 95%
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)*sqrt(1/3/0.129)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.2)
        if edge_on:
            plt.plot(dat[:,0],dat[:,1],'k-',lw=lw,zorder=0.2)
        if text_on:
            plt.text(0.8e-7/1.2,0.2e-12,r'{\bf Dark}',fontsize=fs,color=col,rotation=90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.text(2e-7/1.2,0.2e-12,r'{\bf E-field}',fontsize=fs,color=col,rotation=90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
        return

    def ORPHEUS(ax,col='darkred',fs=10,text_on=True,edge_on=False,lw=0.8):
        # data file is for randomly polarised case
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/ORPHEUS.txt")
        dat[:,1] = dat[:,1]*sqrt(1/3/0.01944939)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor='k',facecolor=col,zorder=0.1,lw=0)
        if edge_on:
            plt.plot(dat[:,0],dat[:,1],'k-',lw=lw,zorder=0.2)
        if text_on:
            plt.text(6.5e-5,0.5e-13,r'{\bf ORPHEUS}',color=col,rotation=-90,fontsize=fs,clip_on=True)
        return

    def WISPDMX(ax,col='crimson',fs=12,text_on=True,edge_on=False,lw=0.8):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/WISPDMX.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)*sqrt(1/3/0.23)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.201)
        if edge_on:
            plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=0.202,lw=lw)

        if text_on:
            plt.text(9e-7,4.1e-12/1.2,r'{\bf WISP}',fontsize=fs,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.text(9e-7,1.8e-12/1.2,r'{\bf DMX}',fontsize=fs,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)

        return

    def DOSUE(ax,col='red',fs=9,text_on=True,edge_on=False,lw=0.8):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/DOSUE-RR.txt")
        dat[:,1] = dat[:,1]*sqrt(2/3/0.29377804)*sqrt(0.39/0.45)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.201)
        if edge_on:
            plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=0.202,lw=lw)

        if text_on:
            plt.text(90e-6,0.26e-10,r'{\bf DOSUE-RR}',fontsize=fs,color=col,rotation=-90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
        return


    def SQuAD(ax,col=[0.7,0,0],fs=12,text_on=True,lw=0.5,point_on=False,ms=10):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/SQuAD.txt")
        dat[:,1] = dat[:,1]*sqrt(0.4/0.45)*sqrt(1/3/0.019)
        plt.plot([dat[0,0],dat[0,0]],[y2,dat[0,1]],lw=lw,color=col,alpha=1,zorder=0.2)
        if point_on:
            plt.plot(dat[0,0],dat[0,1],'o',mfc=col,mec='k',mew=lw+1,zorder=0.2,markersize=ms)
        if text_on:
            plt.text(36e-6,0.25e-14,r'{\bf SQuAD}',fontsize=fs,color=col,rotation=-90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
        return


    def DMPathfinder(ax,col='pink',fs=13,text_on=True):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/DM-Pathfinder.txt")
        dat[:,1] = dat[:,1]*sqrt(1/0.075)
        plt.plot([dat[0,0],dat[0,0]],[y2,dat[0,1]],lw=2,color=col,alpha=1,zorder=0.6)
        if text_on:
            plt.text(2.1e-9,0.5e-8/1.9,r'{\bf DM}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)
            plt.text(2.1e-9,0.2e-8/1.9,r'{\bf Pathfinder}',fontsize=fs,color=col,rotation=0,rotation_mode='anchor',ha='center',va='center',clip_on=True)

        return


    def QuantumCyclotron(ax,col='orangered',fs=13,text_on=True):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/QuantumCyclotron.txt")
        dat[:,1] = dat[:,1]*sqrt(0.3/0.45)
        plt.plot([dat[0,0],dat[0,0]],[y2,dat[0,1]],lw=2,color=col,alpha=1,zorder=0.6,path_effects=line_background(2.5,'k'))
        if text_on:
            plt.text(0.95e-3,1e-10,r'{\bf QC}',fontsize=fs,color=col,rotation=-90,rotation_mode='anchor',ha='center',va='center',clip_on=True)
        return

    def DarkMatter(ax,Witte_col='royalblue',Caputo_col='dodgerblue',Arias_col='navy',fs=20,projection=True,text_on=True):
        y2 = ax.get_ylim()[1]
        zo = 0.3
        pek=[pe.Stroke(linewidth=7, foreground='k'), pe.Normal()]

        # Combined limits
        dat = loadtxt("limit_data/DarkPhoton/DM_combined.txt")
        plt.plot(dat[:,0],dat[:,1],'-',color='w',alpha=1,zorder=zo+0.1,lw=2.5,path_effects=pek)
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor='lightgray',zorder=zo,alpha=1.0)
        plt.plot([1e-16,dat[0,0]],[dat[0,1],dat[0,1]],'--',color='w',alpha=1,zorder=zo+0.1,lw=2.5,path_effects=pek)
        plt.fill_between([1e-16,dat[0,0]],[dat[0,1],dat[0,1]],y2=y2,edgecolor=None,facecolor='lightgray',zorder=zo+0.1,alpha=1.0)
        plt.plot(dat[40:,0],dat[40:,1],'--',color='w',alpha=1,lw=2.5,zorder=1000,solid_capstyle='round')

        # Individual limits
        dat2 = loadtxt("limit_data/DarkPhoton/Cosmology_Witte_inhomogeneous.txt")
        dat4 = loadtxt("limit_data/DarkPhoton/Cosmology_Caputo_HeII.txt",delimiter=',')
        dat5 = loadtxt("limit_data/DarkPhoton/Cosmology_Arias.txt")

        plt.fill_between(dat2[:,0],dat2[:,1],y2=y2,edgecolor='k',facecolor=Witte_col,zorder=0.305,alpha=0.8)
        plt.fill_between(dat4[:,0],dat4[:,1],y2=y2,edgecolor='k',facecolor=Caputo_col,zorder=0.305,alpha=0.8)
        plt.fill_between(dat5[:,0],dat5[:,1],y2=y2,edgecolor='k',facecolor=Arias_col,zorder=0.306,alpha=1)

        if text_on:
            plt.gcf().text(0.295,0.42-0.04,r'{\bf DPDM} HeII',fontsize=15,color='w',ha='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.gcf().text(0.295,0.4-0.04,r'Reionisation',fontsize=15,color='w',ha='center',clip_on=True)
            plt.gcf().text(0.295,0.38-0.04,r'(Caputo et al.)',fontsize=13,color='w',ha='center',clip_on=True)

            plt.gcf().text(0.365,0.37,r'{\bf DPDM}',fontsize=17,color='w',ha='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.gcf().text(0.365,0.35,r'(Witte et al.)',fontsize=13,color='w',ha='center',clip_on=True)

            plt.gcf().text(0.485,0.43,r'{\bf DPDM}',rotation=21.5,fontsize=18,color='w',va='center',ha='center',path_effects=line_background(1.5,'k'),rotation_mode='anchor',clip_on=True)
            plt.gcf().text(0.49,0.41,r'(Arias et al.)',rotation=21.5,fontsize=16,color='w',va='center',ha='center',path_effects=line_background(1,'k'),rotation_mode='anchor',clip_on=True)
    
        return

    def COBEFIRAS(ax,col='#247840',text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat3 = loadtxt("limit_data/DarkPhoton/COBEFIRAS.txt",delimiter=',')
        plt.fill_between(dat3[:,0],dat3[:,1],y2=y2,edgecolor='k',facecolor=col,zorder=0.5,alpha=1)
        plt.plot(dat3[:,0],dat3[:,1],'k-',lw=lw,zorder=0.5)
        if text_on:
            plt.gcf().text(0.29,0.70,r'{\bf COBE/FIRAS}',fontsize=22,color='w',ha='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.gcf().text(0.29,0.67,r'$\gamma \rightarrow X$',fontsize=22,color='w',ha='center',path_effects=line_background(1,'k'),clip_on=True)
        return


    def LSW(ax,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/SPring-8.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=[0.45, 0.05, 0.1],zorder=1.101)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.101,lw=lw)

        dat = loadtxt("limit_data/DarkPhoton/ALPS.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=[0.55, 0.0, 0.16],zorder=1.091)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.091,lw=lw)

        dat = loadtxt("limit_data/DarkPhoton/LSW_UWA.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=[0.6, 0.0, 0.2],zorder=1.09)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.09,lw=lw)

        dat = loadtxt("limit_data/DarkPhoton/LSW_ADMX.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=[0.65, 0.1, 0.24],zorder=1.089)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.089,lw=lw)

    #     dat = loadtxt("limit_data/DarkPhoton/LSW_CERN.txt")
    #     plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.089,lw=2)
    #     plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=[0.65, 0.15, 0.2],zorder=1.089)

        dat = loadtxt("limit_data/DarkPhoton/CROWS.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=[0.7, 0.2, 0.2],zorder=1.08)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.08,lw=lw)

        dat = loadtxt("limit_data/DarkPhoton/DarkSRF.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=[0.5, 0.2, 0.2],zorder=1.06)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.06,lw=lw)

   

        if text_on:
            plt.text(0.4e-6,0.15e-3,r'{\bf LSW-ADMX}',fontsize=17,color='w',rotation=-58,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(1e-5,5e-5,r'{\bf LSW-UWA}',fontsize=14,color='w',rotation=-56,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(0.55e0,0.9e-4,r'{\bf LSW-SPring-8}',fontsize=13,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(1.2e-4,0.9e-5,r'{\bf ALPS}',fontsize=25,color='w',rotation=-56,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(0.75e-7,9.9e-5,r'{\bf CROWS}',fontsize=24,color='w',rotation=-56,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(8.2e-7,0.4e-8,r'{\bf DarkSRF}',fontsize=17,color='w',rotation=-42,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)

        return

    def Coulomb(ax,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/Cavendish.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=[0.7,0,0],zorder=1.07)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.07,lw=lw)

        dat = loadtxt("limit_data/DarkPhoton/PlimptonLawton.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor='crimson',zorder=1.071)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.071,lw=lw)

        dat = loadtxt("limit_data/DarkPhoton/Spectroscopy.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=[0.4, 0.0, 0.13],zorder=1.11)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.11,lw=lw)

        dat = loadtxt("limit_data/DarkPhoton/AFM.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=[0.4, 0.2, 0.2],zorder=1.5)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.5,lw=lw)
        if text_on:
            plt.text(2.5e-10,0.35e-1,r'{\bf Plimpton-Lawton}',fontsize=15,color='w',rotation=-38,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(3e1,3e-1,r'{\bf AFM}',fontsize=20,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(0.5e-8,4e-6,r'{\bf Cavendish-Coulomb}',fontsize=23,color='w',rotation=-39,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(0.2e2,1e-3,r'{\bf Spectroscopy}',fontsize=23,color='w',rotation=-34,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)

        return

    def NeutronStarCooling(ax,col='#004d00',fs=18,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/NeutronStarCooling.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.1001)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.1001,lw=lw)
        if text_on:
            plt.text(0.9e4,0.4e-6,r'{\bf Neutron stars}',fontsize=fs,color='w',rotation=-45,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1,'k'),clip_on=True)
        return

    def CAST(ax,col='maroon',fs=19,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/CAST.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.1)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.1,lw=lw)
        if text_on:
            plt.text(0.95e-3,6e-6,r'{\bf CAST}',fontsize=fs,color='w',rotation=-59,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
        return

    def HINODE(ax,col='#700606',fs=16,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/HINODE.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.1001)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.1001,lw=lw)
        if text_on:
            plt.text(5e-3,0.3e-5,r'{\bf HINODE}',fontsize=fs,color='w',rotation=-59,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
        return

    def SHIPS(ax,col='indianred',fs=20,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/SHIPS.txt")
        dat[:,1] = dat[:,1]/dat[:,0]
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.09)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.09,lw=lw)

        if text_on:
            plt.text(0.6e-1,0.08e-8,r'{\bf SHIPS}',fontsize=fs,color='w',rotation=-32,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
        return

    def TEXONO(ax,col=[0.5, 0.0, 0.13],fs=15,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/TEXONO.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1.101)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1.101,lw=lw)
        if text_on:
            plt.text(0.25e2,0.1e-4,r'{\bf TEXONO}',fontsize=fs,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
        return

    def IGM(ax,col='#236991',fs=18,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/IGM.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.49)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=0.49,lw=lw)

        if text_on:
            plt.text(4e-12,0.03e-7,r'{\bf IGM}',fontsize=fs,color='w',rotation=-39,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
        return

    def LeoT(ax,col='#4a7e91',fs=18,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/LeoT.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.3061)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=0.3062,lw=lw)

        if text_on:
            plt.text(7e-13,0.2e-9,r'{\bf Leo T}',fontsize=fs,color='w',rotation=-39,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
        return

    def GasClouds(ax,col='#436991',fs=18,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/GasClouds.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=0.306)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=0.307,lw=lw)

        if text_on:
            plt.text(0.86e-13,1e-10,r'{\bf Gas clouds}',fontsize=fs,color='w',rotation=-39,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
        return

    def SuperMAG(ax,col='#b5403e',fs=18,text_on=True,lw=1.5):
        y2 = ax.get_ylim()[1]
        dat = loadtxt("limit_data/DarkPhoton/SuperMAG.txt")
        plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,zorder=1)
        plt.plot(dat[:,0],dat[:,1],color='k',alpha=1,zorder=1,lw=lw)

        if text_on:
            plt.text(1.5e-17,1e-1/1.4,r'{\bf Super}',fontsize=fs,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)
            plt.text(1.5e-17,0.2e-1/1.4,r'{\bf MAG}',fontsize=fs,color='w',rotation=0,rotation_mode='anchor',ha='center',va='center',path_effects=line_background(1.5,'k'),clip_on=True)

        return




#==============================================================================#
def MySaveFig(fig,pltname,pngsave=True):
    fig.savefig(pltdir+pltname+'.pdf',bbox_inches='tight')
    if pngsave:
        fig.set_facecolor('w') # <- not sure what matplotlib fucked up in the new version but it seems impossible to set png files to be not transparent now
        fig.savefig(pltdir_png+pltname+'.png',bbox_inches='tight',transparent=False)

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
    plt.rcParams.update({"text.usetex": True,"font.family": "serif","font.serif": ["Palatino"],})
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
    plt.rcParams.update({"text.usetex": True,"font.family": "serif","font.serif": ["Palatino"],})
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


def MyDoublePlot_Vertical(xlab1='',ylab1='',xlab2='',ylab2='',\
                     hspace=0.05,lw=2.5,lfs=45,tfs=30,size_x=15,size_y=14,Grid=False,height_ratios=[2.5,1]):
    plt.rcParams['axes.linewidth'] = lw
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif',size=tfs)
    plt.rcParams.update({"text.usetex": True,"font.family": "serif","font.serif": ["Palatino"],})


    fig, axarr = plt.subplots(2,1,figsize=(size_x,size_y))
    gs = gridspec.GridSpec(2, 1,height_ratios=height_ratios)
    gs.update(hspace=hspace)
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])

    ax1.tick_params(which='major',direction='in',width=2,length=13,right=False,top=True,pad=10)
    ax1.tick_params(which='minor',direction='in',width=1,length=10,right=False,top=True)

    ax2.tick_params(which='major',direction='in',width=2,length=13,right=False,top=True,pad=10)
    ax2.tick_params(which='minor',direction='in',width=1,length=10,right=False,top=True)

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
    plt.rcParams.update({"text.usetex": True,"font.family": "serif","font.serif": ["Palatino"],})
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
