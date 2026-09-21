from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

OUT = Path('output/pdf/okabe-ito-visualization-guide.pdf')
OUT.parent.mkdir(parents=True, exist_ok=True)

OI = {
    'Orange': '#E69F00', 'Sky blue': '#56B4E9', 'Bluish green': '#009E73',
    'Yellow': '#F0E442', 'Blue': '#0072B2', 'Vermilion': '#D55E00',
    'Reddish purple': '#CC79A7', 'Black': '#000000'
}
NEUTRAL = {'Ink':'#17202A','Secondary':'#5F6B76','Border':'#CBD2D9','Canvas':'#F3F5F7','White':'#FFFFFF'}
ORDER = ['Blue','Orange','Bluish green','Vermilion','Reddish purple','Sky blue','Yellow','Black']
MARK_DISPLAY_SCALE = 1.30

plt.rcParams.update({
    'font.family':'DejaVu Sans', 'font.size':9, 'axes.titlesize':12,
    'axes.labelsize':9, 'axes.edgecolor':NEUTRAL['Border'], 'axes.linewidth':0.8,
    'xtick.color':NEUTRAL['Secondary'], 'ytick.color':NEUTRAL['Secondary'],
    'text.color':NEUTRAL['Ink'], 'axes.labelcolor':NEUTRAL['Ink'],
    'figure.facecolor':'white', 'axes.facecolor':'white', 'savefig.facecolor':'white'
})

def mix(c1, c2='#FFFFFF', t=.5):
    a, b = np.array(to_rgb(c1)), np.array(to_rgb(c2))
    return tuple((1-t)*a + t*b)

def page_title(fig, title, subtitle, n):
    fig.text(.065,.955,title,fontsize=22,fontweight='bold',va='top',color=NEUTRAL['Ink'])
    fig.text(.065,.915,subtitle,fontsize=9.5,va='top',color=NEUTRAL['Secondary'])
    fig.text(.935,.955,f'{n:02d}',fontsize=11,ha='right',va='top',color=NEUTRAL['Secondary'])
    fig.add_artist(Rectangle((.065,.895),.87,.002,transform=fig.transFigure,color=OI['Blue'],lw=0))

def clean(ax):
    ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y',color=NEUTRAL['Canvas'],lw=.8)
    ax.set_axisbelow(True)

def adaptive_point_area(points, dimensions=2):
    """Choose mark area from normalized local spacing, not raw axis units."""
    pts=np.asarray(points,dtype=float)[:,:dimensions]
    spans=np.maximum(np.ptp(pts,axis=0),1e-9)
    normalized=(pts-np.min(pts,axis=0))/spans
    delta=normalized[:,None,:]-normalized[None,:,:]
    distances=np.sqrt(np.sum(delta**2,axis=2))
    np.fill_diagonal(distances,np.inf)
    median_nearest_neighbor=float(np.median(np.min(distances,axis=1)))
    return float(np.clip(6+250*median_nearest_neighbor,6,28))

with PdfPages(OUT) as pdf:
    # 1: system overview
    fig = plt.figure(figsize=(8.27,11.69))
    page_title(fig,'Okabe–Ito visual system','A compact, accessible palette for papers, posters, and personal websites.',1)
    ax = fig.add_axes([.065,.58,.87,.27]); ax.axis('off')
    names = ORDER
    for i,name in enumerate(names):
        x=(i%4)*.25; y=.58-(i//4)*.5
        ax.add_patch(FancyBboxPatch((x,y),.22,.34,boxstyle='round,pad=0.008,rounding_size=0.015',facecolor=OI[name],edgecolor='none'))
        text_color = 'white' if name in ['Blue','Bluish green','Vermilion','Black'] else NEUTRAL['Ink']
        ax.text(x+.02,y+.12,name,weight='bold',color=text_color,fontsize=10)
        ax.text(x+.02,y+.045,OI[name],color=text_color,fontsize=9,family='monospace')
    ax2=fig.add_axes([.065,.36,.87,.13]); ax2.axis('off')
    for i,(name,col) in enumerate(NEUTRAL.items()):
        x=i*.2
        ax2.add_patch(Rectangle((x,0.35),.18,.45,facecolor=col,edgecolor=NEUTRAL['Border'],lw=.7))
        ax2.text(x,.18,name,fontsize=8.5); ax2.text(x,.03,col,fontsize=8,family='monospace',color=NEUTRAL['Secondary'])
    notes=[('Primary accent','Blue for links, headings,\nand the focal series.'),('Default sequence','Blue → Orange → Green → Vermilion\n→ Purple → Sky blue.'),('Use yellow carefully','Use for fills or dark backgrounds;\navoid thin marks on white.'),('Accessibility','Pair color with labels, line style,\nshape, or position.')]
    ax3=fig.add_axes([.065,.08,.87,.22]); ax3.axis('off')
    for i,(h,t) in enumerate(notes):
        x=(i%2)*.51; y=.72-(i//2)*.48
        ax3.text(x,y,h,fontsize=11,weight='bold'); ax3.text(x,y-.14,t,fontsize=8.7,color=NEUTRAL['Secondary'],linespacing=1.45)
    pdf.savefig(fig,bbox_inches='tight'); plt.close(fig)

    # 2: tints and transitions
    fig=plt.figure(figsize=(8.27,11.69)); page_title(fig,'Tints, shades, and transitions','Derived ramps extend the palette without introducing unrelated hues.',2)
    ax=fig.add_axes([.065,.50,.87,.35]); ax.axis('off')
    ramp_names=['Blue','Bluish green','Orange','Vermilion','Reddish purple']
    levels=[.90,.75,.55,.32,.0]
    for r,name in enumerate(ramp_names):
        y=.84-r*.18
        ax.text(0,y+.045,name,ha='right',va='center',fontsize=9)
        for j,t in enumerate(levels):
            x=.03+j*.18
            col=mix(OI[name],'#FFFFFF',t)
            ax.add_patch(Rectangle((x,y),.17,.09,facecolor=col,edgecolor='none'))
            label=f'{int((1-t)*100)}%'
            ax.text(x+.085,y+.045,label,ha='center',va='center',fontsize=8,color='white' if j>=3 else NEUTRAL['Ink'])
    ax.text(.03,-.02,'Light fills',fontsize=8,color=NEUTRAL['Secondary']); ax.text(.75,-.02,'Strong marks',fontsize=8,color=NEUTRAL['Secondary'])
    grad=np.linspace(-3,3,600).reshape(1,-1)
    for idx,(name,high,ypos) in enumerate([('Blue–Vermilion',OI['Vermilion'],.295),('Blue–Reddish Purple',OI['Reddish purple'],.205)]):
        ax2=fig.add_axes([.11,ypos,.78,.075]); ax2.set_xlim(-3,3); ax2.set_ylim(0,1); ax2.axis('off')
        div=LinearSegmentedColormap.from_list(f'page2div{idx}',[OI['Blue'],'#FFFFFF',high])
        ax2.imshow(grad,aspect='auto',cmap=div,extent=[-3,3,.28,.72])
        for xv in [-3,0,3]: ax2.text(xv,.12,str(xv),ha='center',fontsize=8)
        ax2.text(-3,.88,name,ha='left',fontsize=9,weight='bold',color=NEUTRAL['Ink'])
    fig.text(.065,.125,'Rule of thumb',fontsize=11,weight='bold')
    fig.text(.065,.088,'Use light tints for areas and annotations. Use the full color for lines, points, labels, and selected states.\nFor signed effects, center the diverging scale on a meaningful reference such as zero.',fontsize=9.2,color=NEUTRAL['Secondary'],linespacing=1.5)
    pdf.savefig(fig,bbox_inches='tight'); plt.close(fig)

    # 3: categorical examples
    fig=plt.figure(figsize=(8.27,11.69)); page_title(fig,'Categorical comparisons','Keep category mappings stable across bar, line, and scatter plots.',3)
    gs=fig.add_gridspec(3,1,left=.12,right=.92,bottom=.08,top=.85,hspace=.48)
    cats=['Method A','Method B','Method C','Method D']; vals=[82,74,67,59]
    ax=fig.add_subplot(gs[0]); ax.bar(cats,vals,color=[OI[x] for x in ORDER[:4]],width=.62)
    ax.set_ylim(0,100); ax.set_ylabel('Score (%)'); ax.set_title('Bar chart · direct comparison',loc='left',weight='bold'); clean(ax)
    for i,v in enumerate(vals): ax.text(i,v+2,str(v),ha='center',weight='bold')
    ax=fig.add_subplot(gs[1]); x=np.arange(1,7)
    for i,(name,base) in enumerate(zip(ORDER[:3],[63,58,52])):
        y=base+np.array([0,5,8,12,14,17])*(1-.08*i)
        ax.plot(x,y,color=OI[name],lw=2,marker=['o','s','D'][i],label=name)
    ax.set_xlabel('Experiment'); ax.set_ylabel('Accuracy (%)'); ax.set_title('Line chart · color + marker',loc='left',weight='bold'); clean(ax); ax.legend(frameon=False,ncol=3)
    ax=fig.add_subplot(gs[2]); rng=np.random.default_rng(8)
    for i,name in enumerate(ORDER[:3]):
        xx=rng.normal(2+i*1.1,.45,22); yy=rng.normal(2.2+i*.55,.5,22)
        ax.scatter(xx,yy,s=32,color=OI[name],marker=['o','s','D'][i],alpha=.85,label=name,edgecolors='white',linewidth=.4)
    ax.set_xlabel('Feature 1'); ax.set_ylabel('Feature 2'); ax.set_title('Scatter plot · color + shape',loc='left',weight='bold'); clean(ax); ax.legend(frameon=False,ncol=3)
    pdf.savefig(fig,bbox_inches='tight'); plt.close(fig)

    # 4: regression and uncertainty
    fig=plt.figure(figsize=(8.27,11.69)); page_title(fig,'Regression and uncertainty','Match hue within each group; separate points, bands, and fits by opacity.',4)
    gs=fig.add_gridspec(2,1,left=.12,right=.92,bottom=.11,top=.84,hspace=.42)
    rng=np.random.default_rng(12); x=np.linspace(0,10,48); y=1.9*x+4+rng.normal(0,3.2,len(x)); coef=np.polyfit(x,y,1); fit=np.polyval(coef,x)
    reg_point_area=adaptive_point_area(np.column_stack((x,y)))
    reg_display_area=reg_point_area*MARK_DISPLAY_SCALE
    ax=fig.add_subplot(gs[0]); ax.scatter(x,y,s=reg_display_area,color=OI['Blue'],alpha=.28,edgecolors='none',label='Observations')
    reference_canvas_area=ax.get_position().width*ax.get_position().height
    ax.fill_between(x,fit-2.8,fit+2.8,color=OI['Blue'],alpha=.16,lw=0,label='95% interval')
    ax.plot(x,fit,color=OI['Blue'],lw=2.4,label='Model fit')
    ax.set_xlabel('Predictor'); ax.set_ylabel('Outcome'); ax.set_title('Single model · one hue, three emphasis levels',loc='left',weight='bold'); clean(ax)
    handles, labels = ax.get_legend_handles_labels(); order=[2,1,0]; ax.legend([handles[i] for i in order],[labels[i] for i in order],frameon=False,ncol=3)
    lower=gs[1].subgridspec(1,2,wspace=.26)
    rng2=np.random.default_rng(24)
    fits=[1.25*x+5,1.9*x+3.5]
    observations=[fits[i]+rng2.normal(0,2.1,len(x)) for i in range(2)]
    two_model_points=np.vstack([np.column_stack((x,obs)) for obs in observations])
    two_model_area=adaptive_point_area(two_model_points)
    two_model_display_areas=[]
    for p,(palette,title) in enumerate([(['Blue','Orange'],'Blue + amber'),(['Blue','Reddish purple'],'Blue + pink')]):
        ax=fig.add_subplot(lower[p])
        canvas_area=ax.get_position().width*ax.get_position().height
        canvas_area_scale=canvas_area/reference_canvas_area
        canvas_length_scale=np.sqrt(canvas_area_scale)
        display_area=two_model_area*canvas_area_scale*MARK_DISPLAY_SCALE
        two_model_display_areas.append(display_area)
        for i,name in enumerate(palette):
            marker=['o','s'][i]
            ax.scatter(x,observations[i],s=display_area,color=OI[name],alpha=.25,marker=marker,edgecolors='none')
            ax.fill_between(x,fits[i]-2.2,fits[i]+2.2,color=OI[name],alpha=.14,lw=0)
            ax.plot(x,fits[i],color=OI[name],lw=2.4*canvas_length_scale,label=['Control','Treatment'][i])
        ax.set_xlabel('Predictor');
        if p==0: ax.set_ylabel('Predicted outcome')
        ax.set_title(f'Two models · {title}',loc='left',weight='bold'); clean(ax); ax.legend(frameon=False,ncol=2,fontsize=8)
    fig.text(.12,.055,f'Data rules stay consistent; marker area and line width then scale to the plot canvas ({reg_display_area:.1f} / {two_model_display_areas[0]:.1f} pt² shown).',fontsize=9,color=NEUTRAL['Secondary'])
    pdf.savefig(fig,bbox_inches='tight'); plt.close(fig)

    # 5: heatmaps
    fig=plt.figure(figsize=(8.27,11.69)); page_title(fig,'Heat maps','Choose the scale from the meaning of the data, not from decoration.',5)
    gs=fig.add_gridspec(2,1,left=.12,right=.88,bottom=.12,top=.84,hspace=.55)
    rng=np.random.default_rng(4)
    data=np.cumsum(rng.uniform(.1,1,(7,10)),axis=1); data=(data-data.min())/(data.max()-data.min())
    seq=LinearSegmentedColormap.from_list('seq',['#FFFFFF',mix(OI['Blue'],'#FFFFFF',.62),OI['Blue']])
    ax=fig.add_subplot(gs[0]); im=ax.imshow(data,cmap=seq,aspect='auto',vmin=0,vmax=1)
    ax.set_title('Sequential · magnitude from low to high',loc='left',weight='bold'); ax.set_xlabel('Time'); ax.set_ylabel('Group'); fig.colorbar(im,ax=ax,fraction=.03,pad=.025,label='Normalized value')
    diff=rng.normal(0,1,(7,10)); lim=np.max(np.abs(diff)); lower=gs[1].subgridspec(1,2,wspace=.24)
    div_specs=[('Blue + vermilion',OI['Vermilion']),('Blue + reddish purple',OI['Reddish purple'])]
    bottom_axes=[]
    for p,(title,high) in enumerate(div_specs):
        div=LinearSegmentedColormap.from_list(f'div{p}',[OI['Blue'],'#FFFFFF',high])
        ax=fig.add_subplot(lower[p]); im=ax.imshow(diff,cmap=div,aspect='auto',vmin=-lim,vmax=lim)
        ax.set_title(f'Diverging · {title}',loc='left',weight='bold',fontsize=10)
        ax.set_xlabel('Condition')
        if p==0: ax.set_ylabel('Group')
        bottom_axes.append(ax)
    cax=fig.add_axes([.905,.13,.018,.275]); fig.colorbar(im,cax=cax,label='Effect')
    fig.text(.15,.06,'Sequential: one direction.  Diverging: meaningful midpoint.  Categorical: distinct classes only.',fontsize=9,color=NEUTRAL['Secondary'])
    pdf.savefig(fig,bbox_inches='tight'); plt.close(fig)

    # 6: 2D embedding
    fig=plt.figure(figsize=(8.27,11.69)); page_title(fig,'2D embedding','For PCA, t-SNE, or UMAP: mark size adapts to point count and dispersion.',6)
    ax=fig.add_axes([.10,.24,.82,.58])
    rng=np.random.default_rng(31)
    specs=[('Blue',(-2.2,.5),(.95,.42),-18),('Orange',(.2,-.55),(1.05,.48),22),('Bluish green',(2.1,.65),(.85,.55),-12)]
    legend=[]; prepared=[]
    for name,center,scale,angle in specs:
        pts=rng.normal(size=(190,2))*scale
        th=np.deg2rad(angle); rot=np.array([[np.cos(th),-np.sin(th)],[np.sin(th),np.cos(th)]])
        pts=pts@rot.T+np.array(center)
        prepared.append((name,pts))
    all_2d=np.vstack([p for _,p in prepared]); base_area=adaptive_point_area(all_2d)
    for name,pts in prepared:
        shades=rng.uniform(.02,.46,len(pts)); colors=[mix(OI[name],'#FFFFFF',t) for t in shades]
        ax.scatter(pts[:,0],pts[:,1],s=1.25*MARK_DISPLAY_SCALE*base_area*rng.uniform(.75,1.25,len(pts)),c=colors,alpha=rng.uniform(.86,1.0,len(pts)),edgecolors='none')
        legend.append(Line2D([0],[0],marker='o',linestyle='none',markerfacecolor=OI[name],markeredgecolor='none',markersize=6,label=name))
    ax.set_title('Three groups · stable hue, varied lightness',loc='left',weight='bold'); ax.set_axis_off()
    ax.legend(handles=legend,frameon=False,ncol=3,loc='upper left')
    fig.text(.10,.16,'Variation should stay within a narrow tint range. Hue identifies the group; random lightness adds depth without creating new categories.',fontsize=9.2,color=NEUTRAL['Secondary'])
    fig.text(.10,.105,f'Adaptive example: {len(all_2d)} points use a displayed base area of {1.25*MARK_DISPLAY_SCALE*base_area:.1f} pt². More points or tighter packing makes marks smaller.',fontsize=9.2,weight='bold',color=OI['Blue'])
    pdf.savefig(fig,bbox_inches='tight'); plt.close(fig)

    # 7: 3D embedding
    fig=plt.figure(figsize=(8.27,11.69)); page_title(fig,'3D embedding','A quiet floor plane and soft projected shadows clarify depth and overlap.',7)
    ax=fig.add_axes([.04,.16,.92,.70],projection='3d')
    rng=np.random.default_rng(52); groups=[]
    for name,shift in [('Bluish green',(.0,.55,.55)),('Reddish purple',(.15,-.5,.15))]:
        u=rng.uniform(-2.7,2.7,220)
        x=u+rng.normal(0,.22,len(u))+shift[0]
        y=.28*u+rng.normal(0,.42,len(u))+shift[1]
        z=1.25+.22*(u**2)+rng.normal(0,.32,len(u))+shift[2]
        x*=.88; y*=.88
        groups.append((name,x,y,z))
    all_3d=np.vstack([np.column_stack((x,y,z)) for _,x,y,z in groups]); base_area_3d=adaptive_point_area(all_3d[:,:2])
    xlo,xhi=np.min(all_3d[:,0])-.10,np.max(all_3d[:,0])+.10
    ylo,yhi=np.min(all_3d[:,1])-.10,np.max(all_3d[:,1])+.10
    floor_z=-.08
    floor=[(xlo,ylo,floor_z),(xhi,ylo,floor_z),(xhi,yhi,floor_z),(xlo,yhi,floor_z)]
    plane=Poly3DCollection([floor],facecolor='#F8F8F8',edgecolor='none',alpha=.58,zsort='min')
    plane.set_sort_zpos(-10); ax.add_collection3d(plane)
    zmin,zmax=np.min(all_3d[:,2]),np.max(all_3d[:,2]); shadow_rgb=np.array(to_rgb('#313840'))
    for name,x,y,z in groups:
        height=np.clip((z-zmin)/(zmax-zmin),0,1); near=1-height
        outer_rgba=np.column_stack((np.tile(shadow_rgb,(len(z),1)),.006+.028*near))
        core_rgba=np.column_stack((np.tile(shadow_rgb,(len(z),1)),.012+.075*near))
        ax.scatter(x,y,np.full_like(z,floor_z+.012),s=base_area_3d*(2.0+1.8*height),c=outer_rgba,depthshade=False,edgecolors='none')
        ax.scatter(x,y,np.full_like(z,floor_z+.018),s=base_area_3d*(.75+.45*near),c=core_rgba,depthshade=False,edgecolors='none')
    legend=[]
    for name,x,y,z in groups:
        shades=rng.uniform(.02,.44,len(x)); colors=[mix(OI[name],'#FFFFFF',t) for t in shades]
        ax.scatter(x,y,z,s=1.25*MARK_DISPLAY_SCALE*base_area_3d*rng.uniform(.75,1.25,len(x)),c=colors,alpha=.97,depthshade=False,edgecolors='none')
        legend.append(Line2D([0],[0],marker='o',linestyle='none',markerfacecolor=OI[name],markeredgecolor='none',markersize=6,label=name))
    ax.view_init(elev=25,azim=-56); ax.set_box_aspect((1.5,1,.75))
    ax.set_xlim(xlo,xhi); ax.set_ylim(ylo,yhi); ax.set_zlim(-.1,4.2); ax.set_axis_off()
    ax.legend(handles=legend,frameon=False,ncol=2,loc='upper left',bbox_to_anchor=(.06,.93))
    fig.text(.08,.105,f'Height-aware projection: low points cast darker, tighter shadows; high points cast lighter, broader shadows. Point area: {1.25*MARK_DISPLAY_SCALE*base_area_3d:.1f} pt².',fontsize=9.2,color=NEUTRAL['Secondary'])
    pdf.savefig(fig,bbox_inches='tight'); plt.close(fig)

    # 8: recipes
    fig=plt.figure(figsize=(8.27,11.69)); page_title(fig,'Ready-to-use recipes','Small, consistent subsets cover most academic and web work.',8)
    ax=fig.add_axes([.065,.12,.87,.72]); ax.axis('off')
    recipes=[
      ('Two groups',['Blue','Orange'],'The safest default comparison.'),
      ('Three groups',['Blue','Orange','Bluish green'],'Balanced and clearly separated.'),
      ('Four groups',['Blue','Orange','Bluish green','Vermilion'],'Add labels or shapes\nas a second cue.'),
      ('Positive / neutral / negative',['Bluish green','Black','Vermilion'],'For semantic states,\nnot ordered magnitude.'),
      ('Website accent',['Blue'],'Pair with neutral surfaces and text.'),
      ('Poster highlight',['Orange','Blue'],'Orange attracts attention; blue anchors structure.')]
    for i,(title,names,desc) in enumerate(recipes):
        y=.93-i*.155
        ax.text(0,y,title,fontsize=10.5,weight='bold',va='center')
        for j,name in enumerate(names):
            ax.add_patch(FancyBboxPatch((.40+j*.075,y-.033),.058,.066,boxstyle='round,pad=0.004,rounding_size=0.008',facecolor=OI[name],edgecolor='none'))
        ax.text(.74,y,desc,fontsize=8.1,color=NEUTRAL['Secondary'],va='center',linespacing=1.35)
        ax.plot([0,1],[y-.077,y-.077],color=NEUTRAL['Canvas'],lw=1)
    fig.text(.065,.075,'Final check: grayscale legibility · sufficient text contrast · stable category mapping · no color-only meaning',fontsize=9.2,weight='bold',color=OI['Blue'])
    pdf.savefig(fig,bbox_inches='tight'); plt.close(fig)

print(OUT.resolve())
