import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size':4.3,'font.family':'Arial Narrow','axes.linewidth':0.4,
  'xtick.major.width':0.3,'ytick.major.width':0.3,'xtick.major.size':1.2,'ytick.major.size':1.2,
  'xtick.major.pad':0.6,'ytick.major.pad':0.6,'axes.labelpad':0.5,'lines.linewidth':0.7})
B,O,G,R,K='#2a78d6','#eb6834','#1baf7a','#e34948','#555555'
def fig(w=0.84,h=0.72):
    f,ax=plt.subplots(figsize=(w,h),dpi=400); ax.spines[['top','right']].set_visible(False); return f,ax
def save(f,n,t):
    f.axes[0].set_title(t,pad=1.2,fontsize=4.5,fontweight='bold'); f.tight_layout(pad=0.15); f.savefig('img/'+n,dpi=400); plt.close(f)

# 1 monopoly p=100-2Q, MC 20
f,ax=fig(); Q=np.linspace(0,50,2)
ax.plot(Q,100-2*Q,B); ax.plot([0,25],[100,0],O,ls='--'); ax.axhline(20,color=K)
ax.fill([0,20,0],[100,60,60],color=B,alpha=.25); ax.fill([0,20,20,0],[60,60,20,20],color=G,alpha=.3)
ax.fill([20,40,20],[60,20,20],color=R,alpha=.3)
ax.text(3,70,'CS',fontsize=4); ax.text(6,36,'PS=π',fontsize=4); ax.text(22,28,'DWL',fontsize=4)
ax.text(31,44,'D',color=B); ax.text(22,6,'MR',color=O); ax.text(44,23,'MC',color=K)
ax.set_xticks([20,40]); ax.set_xticklabels(['Q*','Qc']); ax.set_yticks([20,60,100]); ax.set_yticklabels(['c','p*','a'])
ax.set_xlim(0,52); ax.set_ylim(0,105); save(f,'mono.png','Monopoly: MR = MC')

# 2 price taker P=30, MC=4+2q
f,ax=fig(); q=np.linspace(0,18,2)
ax.plot(q,4+2*q,K); ax.axhline(30,color=B); ax.fill([0,13,0],[4,30,30],color=G,alpha=.3)
ax.text(2,22,'PS',fontsize=4); ax.text(15,32,'P = MR',color=B); ax.text(15.5,41,'MC',color=K)
ax.set_xticks([13]); ax.set_xticklabels(['q*']); ax.set_yticks([4,30]); ax.set_yticklabels(['m','P'])
ax.set_xlim(0,20); ax.set_ylim(0,45); save(f,'ptaker.png','Price taker: P = MC')

# 3 elasticity along Q=120-2P (P on y)
f,ax=fig(); P=np.linspace(0,60,50); ax.plot(120-2*P,P,B)
ax.plot(60,30,'o',ms=1.6,color=K); ax.text(62,31,'|ε|=1 (mid)',fontsize=4)
ax.text(10,50,'elastic |ε|>1',fontsize=4); ax.text(78,8,'inelastic',fontsize=4)
ax.set_xticks([60,120]); ax.set_yticks([30,60]); ax.set_xlabel('Q'); ax.set_ylabel('P')
ax.set_xlim(0,125); ax.set_ylim(0,63); save(f,'elast.png','Elasticity on a line')

# 4 kink q_H=100-p, q_L=60-p
f,ax=fig(); p=np.linspace(60,100,10); ax.plot(100-p,p,B)
p2=np.linspace(0,60,10); ax.plot(160-2*p2,p2,B); ax.plot(100-p2,p2,B,ls=':',lw=.5)
ax.plot(40,60,'o',ms=1.6,color=R); ax.text(43,63,'kink (40, 60)',fontsize=4)
ax.text(5,88,'only H',fontsize=4); ax.text(95,22,'H + L',fontsize=4)
ax.set_xticks([40,160]); ax.set_yticks([60,100]); ax.set_xlabel('Q'); ax.set_ylabel('p')
ax.set_xlim(0,165); ax.set_ylim(0,105); save(f,'kink.png','Kinked demand')

# 5 simultaneity full width
f,ax=fig(1.68,0.72)
for d in (0,30): P=np.linspace(0,40,2); ax.plot(100+d-2*P,P,B,lw=.5)
for s in (0,30): P=np.linspace(max(0,(20-s)/4),40,2); ax.plot(-20+s+4*P,P,G,lw=.5)
dpts=[(60,20),(80,25)]; spts=[(60,20),(70,15)]
ax.plot(*zip(*dpts),color=R,ls='--',lw=.6); ax.plot(*zip(*spts),color=O,ls='--',lw=.6)
for x,y in dpts+spts: ax.plot(x,y,'o',ms=1.6,color=K)
ax.text(82,26.5,'demand shift → points trace SUPPLY (slope +)',fontsize=4,color=R)
ax.text(72,12.5,'supply shift → points trace DEMAND',fontsize=4,color=O)
ax.text(101,2,'D',color=B); ax.text(131,2,"D'",color=B); ax.text(121,37,'S',color=G); ax.text(160,37,"S'",color=G)
ax.set_xlabel('Q'); ax.set_ylabel('P'); ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(30,170); ax.set_ylim(0,44); save(f,'simult.png','Simultaneity: use a supply shifter (instrument) to trace demand')

# 6 Cournot BRs a100 b1 c10
f,ax=fig(); x=np.linspace(0,90,2)
ax.plot(45-x/2,x,B); ax.plot(x,45-x/2,O,ls='--'); ax.plot([0,45],[45,0],K,ls=':',lw=.5)
for (a,b,l,c) in [(30,30,'Cournot','#1baf7a'),(45,22.5,'Stack.','#6250d6'),(22.5,22.5,'Mono','#e34948')]:
    ax.plot(a,b,'o',ms=1.6,color=c)
ax.text(31,32,'Cournot',fontsize=4); ax.text(46,24,'Stackel.',fontsize=4); ax.text(2,14,'Mono split',fontsize=4)
ax.text(2,82,'BR1',color=B); ax.text(70,8,'BR2',color=O)
ax.set_xticks([0,30,45]); ax.set_yticks([0,30,45]); ax.set_xlabel('q1'); ax.set_ylabel('q2')
ax.set_xlim(0,92); ax.set_ylim(0,92); save(f,'cournot.png','Cournot BRs (slope −)')

# 7 Bertrand BRs d40 c10
f,ax=fig(); y=np.linspace(0,40,2)
ax.plot(15+y/4,y,B); ax.plot(y,15+y/4,O,ls='--')
ax.plot(20,20,'o',ms=1.6,color=G); ax.plot(25,25,'o',ms=1.6,color=R)
ax.text(5,21,'Bertrand',fontsize=4); ax.text(26,27,'Merged',fontsize=4)
ax.text(26,38,'BR1',color=B); ax.text(33,22,'BR2',color=O)
ax.set_xticks([0,20,25]); ax.set_yticks([0,20,25]); ax.set_xlabel('p1'); ax.set_ylabel('p2')
ax.set_xlim(0,42); ax.set_ylim(0,42); save(f,'bertrand.png','Bertrand BRs (slope +)')
print('ok')
