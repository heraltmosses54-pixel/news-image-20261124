#!/usr/bin/env python3
"""THE WORLD — Tuesday 24 November 2026 in one image.
Dense broadsheet front page: 23 stories, six continents, one page.
Pure stdlib; embedded font atlas; deterministic; no network.
Writes entry.png to $MAKEFUN_OUTPUT_DIR (fallback: cwd)."""
import base64, os, struct, zlib

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GREY = (90, 86, 78)
CARD = (255, 255, 255)
LINEC = (198, 192, 180)
MAPDOT = (148, 163, 188)
MAPBG = (233, 236, 240)
WHITE = (255, 255, 255)

PX = bytearray(PAPER) * (W * H)

def rect(x, y, w, h, col):
    if w <= 0 or h <= 0:
        return
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(col) * (x1 - x0)
    for yy in range(y0, y1):
        i = (yy * W + x0) * 3
        PX[i:i + len(row)] = row

def hline(x, y, w, col, t=1):
    rect(x, y, w, t, col)

def vline(x, y, h, col, t=1):
    rect(x, y, t, h, col)

def save_png(path):
    raw = bytearray()
    stride = W * 3
    for yy in range(H):
        raw.append(0)
        raw += PX[yy * stride:(yy + 1) * stride]
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

FONT_B64 = (
"c-rl~37A{Ol`me}ceRX-&0@Dj-T)ziZt<Tb6B68NvxQ)2K{9z+2rV-6z6rr`H_6QWGa;b`NhTXaO)@h)7F!CLuw-H+2n0xiB?x9qXtfs>+tBK6+Yqq3uY2Dl)%%@ObtQGX4JMP!oA-UAmg-iWs$0vcb55Oes_t#K-*%Z@h-lR9@kGyYyF9JuxZQ|(+!S*na8cl)To2{itrXaOEmThDdOcLcWtP)-_{{oT1oL=WR1t2-@2A$NA(y)vbGf4Dxt-qDwJs;cT;AwfhS?p6QBvjFs0TK?zXc6(5`o|AYDF%BYAsyBc@8^ZPO8u0poXeNyj}zxb5S{`YLbhXeLjl7Znd_4*lx2$5xAn~+pW&l^BvSbrxUq8AJ^wYcda(S>^4H3CHf(U&DXk?1H0X;YPo<>=XG;;QN-^@AbkBoSPsU7`0|&9@Lx6{Z2i8txJ|4VK`BQay~3NgM~I6>q4Iz~=FV>wYjDXH<PLw#F|btxE|1v<3ze-xTr_m2bN`YL1yNOt5aJS{u9PM?<rjv3F1A`OPHz>~y}08k{2o?Uq%9YB7b-s&1vv|l`WEDLUA$C~V|B@VHI6T8e^6|=)b>Ma&UT2~_seq-c@hwR6j?jPMZ*uFtmC&aak;(}q^wKflHY26#KOOwwt<cDt>TjCR{K7&^^&M~Zm$qMS#<vw=z>3ukv)rIE4%CaRsSu>nVyiyo&K~qeekJX_jRXV6xlZT<R?BHJUzN6Hu$8c7ZD)_p9IdrJt4<$Ulx}?J>dB5g^A0bY&!P0(OWNn((?LmqwZIp6peXt`OwW`L+m|yj4trk80Kxjx9evVAxNCExJ;pZ^H$5FTg9~qDPE7WBi3;%L1M_tipz~ON`4+c@hDa1kDZ7CUW-ejAhZ71+0m_Hy+0;)ZWXSqZOcpICCmS6M&Xyk!n$!+NLYa!`}QALf8p4&E7TyRM9mnb*oohfBYTB&OGI2f@ABoX!t+m0*!Q~nwu-w!kxZJwh-FaR3SwodCGurDwhVy`h_b&dXkylgRlSyxVB`}&bL4&TZ~TM1+m(Le!~U3UTW_E-BwkPZzbeFIarZ7Ey26f0j9u)sZ}W7ETQ3fYRr`eSqN<DU5tf~e5l^=x59q`92-~*C2$&%M9U*>#b{pfW|8>7MDW@^~K_Qv|ct!{h$mR1PVFTr?Lh%kMXZ@82z#w^)53e`Inj(R<+nwX?p&O&yg;3v@db(d(^7KxzZii?>h&UjYjZgY+es_})>rgqydh>CX&7d52LWpnC<-KqIZ-3_{U+We3tP^g!AVomS<`=~y$2{32oc~-Io;w5Req_nVESM?FmiV`XH|CY2-kA8Ys0G$7_a>gU|L$zz{d!(}3l~ZO*eS%1osla-?>$)S>We+ydzNh7A-=S|?z=<mP#>`a&Fz@?x7{+Zrn7qccH7SFXGdPzE?!ND9Z!qxE92WOPwl9FUh4V&mh_%uUODOKJ3s+fZ5RJ4KDQuPv;)>HTg5Z>!8O8z5&R=A38V<PC}yj@InuyQ6yx&Z^Ls)&QC9uAUQL`G{^%JY;rJzxbN2<Idt7}#3`8)@jEwIP97C{G*!$uG;+u8fTOPK*{=qkI`Lb|d-!FFfVi$|gc{(ivgTnhOA==~Olj1qCy~*;bwLft3?I))_pZ)k%amP=WZH!nCieVvkA-gHODss6uA%2<{_6dNtiQ7Esi$ng{=TPZ@*x`*|F4lQF#m)iY-XlbFOjtqGw+c}TiFP?B#Ls~jajmd#6K8})7a*Hn6t^$k8;p3qe@I;2EF4eZf>bwvl$V)iJRJ7zlGFArPl_KoK=u#};7>>n@e_y_A#N99wUlw&eOtxXhzY>6w(TPMI%M_>K<Ujl*j{k-JO%!JQ;2_0i%)`mSESwXFWd62G?=AdxYESaUReQQ5_yXI4uZ3;2n!Mk-fO<^*z4#48(jW|xH$4rv@TwMHPL+k%4^2O<$<Up``sl^i%l;J$e{!Y8S!a!p;K7Ez1MPQZ3-pUEia2ltuJ7(iCe8ZErn_EwB_Mu;mp2ndBnD57xG^a&)5c=g!hJi@$Z4e"
"n(TWI+)AVQ!irvN&jaG_yWQP)`Gvdt+aP$3ejBlGf4do<rd6W3+1b<m?j<h@@sMz5F&=Rj$yXY}-NJPs<mk3O{!Q_?xX_;dhCuYasN}$jryc-dUBB&1LgYVeON(z<5d8oZ7YXr!q4-lbTtAo)UwKei?|nifzI5je4_`EtKo-7F;PWr^*D>e1ruQmuY)3G>!yCIw^tw79u%`o|AG;I(=uZ4Nuq+K(v`Tzd{F~^tr#-Pi=mX-P#1j~g_&j>sc;@v?G$Mdm@O&xl`Aokj{X~=SJSU!AvLS7`?~T(F!UfXTznlaW)ulV+BqmYH$$(vHgkG<g6cR7=JBs-{UQ+VBq#PmeRbh531@-{+JCB*`_tI^Y^!dC|eTUB<RWOu;HtF@Ys3cb(3{q<p<6JKnal51EdE8Kw+%6T1u4S0R$uS>bE>fbbtVso1P|i#S{q9!eQef7?6`bdExJd=%TBr>w;-(@#9|DfKshmqS$wkbOtH84ejLW&TE_V?$!q$r%HaC<(o2&JFr`5ZbmDO_s0lqgtowP$EbRcjzEYS-cc0V*i4jg{15i;uhUQg?}E*FXfg9wCmj;MAEcq;f|(9fssy-?GzDq9CYs%|MOA*_$SPACh`Ua+-gJS7iAZWqV*-Y#sTxaL!`jP!~@aQjR6y^Q!?l!=PtdUi)Fdm_uS-d@rSK^3AoY6hI-3@##$>)RbkRrbU^S<9!hsHW*EES~?4h<g_zHzDGEG%GBx-7b#Z<B>x@7bz*9&9aQ4WfrMhYbm;*=K#LHzDUV4zX&eq<eoTsu=E>;cd|Ge#H#%h%J_+8&zaWeQ23Q=aAV79SsuHNpcy$IQj1hSVzIw_ZTmMTfXCl?vi8@-?T*)k=V9m{n;_9WzkM8?T=_V9iQsmz@^N(6_xSwYAAW&~k?I!i*^T`ou=}>3i*>i%_9=1qZMOwa8o2E?&o|Sz-DZ0=dfRQ{d4WLaAk`^ajvo%$Ms9lsk$)RR#FuV4KE38oM{X0hBVzp>B5vdOv}hc`OhM6Gb*FW6h%ob<fH-&d6VBS+H4gP>lyJB~Y=(qQTXu)vvrSkwLi0>jUiM^dzq_616Vtio+j1zea4z0?&BpyCO1~GT@K@9bYO=kI8r{99@+L&iP5>!sM6QSe@>Oc=B}AM9;--V0;-`^Q<77mLH}G=|-4zy=kN05K#U@Jk`&w<k5oh(i%)0C}wJwe}z$)18>lThfi$*rM^TM5Py2h~|)o&I5j#X&<k`Q_w=oEoYcdxi4WF4nv^ic~4;))f(M{qsZ(`{g=#Ik7Nps<cLM{Io|M}MHxb$iT{^<;hjGZE-?^auYW-yE@yoh=4X?xlYe57BD;kofjXsB2JMGKPh@R|NZoFD?8D>wa+uDqM!8+xJ)}*@qZ`a~KUZeG=31oaIH~+J;qkO+<L}=;@j>UlM_YebAE^o~^hk@VXwhvwuOP1z3ZwYoA1)-ylv0_^}Y?D*{vi>uWHgRcOM2auv7SjV6yrc`<0+Y>Wr47yDL+t>eMY)5q;SFYbGUv{(ImbmPk+7e71xO9-V$U;)yP;skqi^Y4UMe<1SJ=wE_=t)u7$>U|As(oS2#+4nQSi@yGC+I6q{iQ{HK0=t^S;@;+vxR>Gtqdc+xV9fPv+Y7;{xVCwCxJ)&XP;l+H{H<6&biLR#W*;DZJ|pw4yg2;(HVwem7Ejr(JPyQoAcBGU5<EWNt*<7w#MXQ&EpB~8xc@yNzEiuT@3}|Zqd$WFgt%wnpXG%$>AKny_Wh4I_WAy4uXt=w_%<iRBWEOhi8B(9h%*xR)ILDm2}AKMu}faC5B@^<yTuESkiPWPkwQ#@Z@+E-FNEjzc|D{HjmN!X#Q?_o495K(`cd4y!^LBLy9unH?6;kyx(R)B(=T5Wzo3ynQVs0TF<-NM0k?_GUl-zi&tnoFd4Kqf`1+wvsL=SPU<Prd`h}uq*)sZ+@Z1p>w^lFS+dIXxUk!J4Z+iJ&7|FLaM#X+_x1-<Q@9h@*8zbU2K-a+X3yg|OM03KG-RpQoJnZYdWgr;&PT&I{?Y9s1|KqhH"
"c$@7vonlKoxL3Hx#1^rt)4I>T7Z|?@jOd4^+O%JYXE%i0z25Aah~=eElc68A?DM3Zy|w{=LOcyTtp6@(5#>B!HZ(8Rghk*r=DDn}zE1K}{8WgqhQt*S(G({hn-iBGjN11v-wU>X6l8o;LriR-AH@kqc~r(xh&g|NMF@Ffk&9i*nbTgq(|hUh1MKl35w%f>>ms#pP|B&}`nI|*bs!Hi&9T=i(N`x~*H9;a@*~TJkKDHhqP+vDGk$?le>e?`<R`+B_ogk|A^BiU%Me=<d<P<3vf|3J?(Q1i9sa8&n~)8G29YXW{*h(V|F~~=*s}3u%kI$M+=Ti-`>)^ka&W(G*KXl_BP}+piJhHTH`H06)xe5zpiltB0r>!#))*76em2^P#cvwwbnmdej+%esgq13i6-vJdG<_An8$CO)#L(&iLiRr490Up;!S7dy4_P+8iHfO8%WIC<d-Ik}FNdzXu6;%RXQKVs5u#?t$X9%kYP>!45<X8ogrU52(NO$O2W0bp0nvI#$T}kI<lCZ<zOTl`s*u>(6!yl&8R9NGrn%P}hv^zvJNV5Hz9cSw@q>X&VRZY??DupESE5nef)e6|RT1%^usz=?yr?TJ+{LZ#C+@uYX|HhqIxSp1X!^%53a|U#)*roeTHn)Dgi78*pN8W*M>uGcG0QejqA|Q4eD(<bZWW&wjbTs1vh5bp81i<4Fh?w7mNDCiv)9|%7`laR=AEL6jJStT#F2%$6AasW#kYk&Dz3XuoIrj^@BPPP8egPgdPxTmP+x?&@$9stHyB-+{oj`T!uNd0v(s|jHuQBD7JX$t%?r9fD`SggfQX_*NK%fQerb=_^hPTOsYiKdb>LM_Q*ue$C~)}53Ndp@cUHOHYAs%`&#aF<&(#XJp+JDjv9sIjX;Cq^+r@@JtMW#ZmcN!^WIwE><auNRthL)Ha0Fn5xXq;B=OQbFoYQ74Tmh^Q(-G}-x})cMD3^=)d}ho|<&-<yJ<m6P6oJELZT+yrZjU1Hpr^1x5Rkv#Rr9|4$j%_Yw8KVLh&B2lhn@V=6p+uIYq@|?x6m&gkYN&C&^}TH=sL!lF<~!zW`uXfUJ;F$zi3AmvLe?hng@!N-JxPEl`h8GdyBDTx+p7=VytbT7z>W^m5h(G`gV&ec3QiG;B>nLHMIBZ2thbYoHe{h6f3(TfeFWOv>0=i0~2C3su1#G6(I;^4eySKqLgRgPUHsYA}fLVl#IS*K53X|^&O0(+0WMX$SwCtVXXkt+<(PRjP$JGR}#gTy)y3y-RLmbrzdLP80tqW3xjCez~-MJzH&A&v2s=v*UySTWsbTQ6@gL(Bl<)IL-!E!I1uxDyl{M@qNP-v5t&l4Z^=-p*!88UQt^X*50;95AwOCwMqafe5N43KRf-e%4dIvi>q_zL9hKsr&s2($9{k$z^H;=0!%qok>7-0|<G5%XYda+TQ<x;*G{+dmx#CkOSA=p{jCJLUF`5_pA<i&`UB>WRS2(6COpA+*X_Bh5BqWlZHFD}e^{GTr0$G<8<4E^|q<~+~oMrRy6aKxn@2>_C1<PL-E-AN*QwuW?a<jfx@1(cyV5h+gmV|2C09o`F5mY#{*e@6NPIcVhwAb0QCkjGu8R*E1WV&$_Q|X<yRTM)AgS2;M5@r`-oUU$nNpw6|5`})xRO3jn5XIlQ6H}}EJ=0w)0dN0hep51Gt-Rr=OyG`KGj7VD-d@o*AaaRJx+8BXUbh!I!nCT<S(z2qVQ@h%(KgW0D^h9Sj0j9wjc772x^@glgujBKHiL}jT<5}oL@rc*1K28ne3IyPTM4RuB`kcBRFO1$!(})icSHKOL+}R=x%=d3`{TjU_WL_VJ%$`LkW>B1H-vF>Dq%!gdX3QPLwuz);FgWQ6NUIWZF%7Yb>o86M+u0@nKpmc9yuM@*EHRh_e^(W-F&6A4R9>kVgJ6S-nOh~0==4ULwEf9tUs`9JP@;P8TU*H9}po&5ia<0t>X)7-K%PaVm9T9t{Jr6w>yF%1V?xzL0L%~H|I8tx@L?}*QSx$1(tPi1flw("
"EZsr3ajZUQ>D}<8n1`Jug}8D0q%aDd!l;CVk$PMh$Il@zm#)^RzETeLyxB0_ICtWt3>V_b<cM$FJuO4IXnhoTeKR<7;-nFt*Tqm*H*ga1?^`w4mUmBgq+PRg4IpjVd?4~xlT_c`x0;LkIWuJ6tS}<AfeTmPL$(>~_uICDe8GUra$mf`GwJMkS@_3AK~5o5U*EX!P6}Jkc*7z0^!%TPC(Pa_r&DpyWJ@+U5EyAoyQWexYiSt73sUVE6CH_;MAz3!-Z}4hu>Y0*VUcO?=*YWD{jW@mmN_pZsFCOx5bgP<LC;h!W<f_q*O;&jmp~S&&aUjLy%|*BmPhrYZCTfJGHw~_3yBO-D6HWi6z4YB-UmX&D{;{=A=b=^RppSs5^>5HF-Keg)t-qn`WwO2ZF$#Bd)_riS4tC{@>4Rw$Vx79NlKZpK_~V`y1=CkWCw$y3f;noPGqveT?&zFeB659o`^fr1zuf^GF`A`u{MyK0HXih;VTB5Jy`whXlNCF_hk}}sbr!tpG<T_@RPE{?cwK>ve$<e_*XeVCO+*6OsZe|z-ozlE;2?OZ-ztwWttBT#apIVPBf3XW`d)xY1j11z2d6}qcC6~Gn&UyCwSS2Ll~h7469{8X@^EcST`Sx`6pKGZ5Z)Q_$F2jT8oufVDHL(ExqpP#=R>iY+DY-t()Hr`S-TuTk?VNwtQf!ac|4CZOf}u=-n9E9sbHoB6rca4}Zb@nuur8Gs%8=K{5Zf)zQ>dlPZ~tw>?>EdvdP%htpWw+Vah`0p2t~9kUrR$VjsH=o7@n2n)}_h;2}8IKCHF@=eY|>jmPE!}9SQeE$!6$WmK*GYqw-g7IgCEAL0VF=7MU-Yu;6$wU4Zx<&BKG~{q4VJ`v~&fiW6`z_<a;e&B1L%(P6X<PaAk!RXM?eaW1?!pi{Ix~@C$PmR)CeqOv%)7>)7ww(FUf-x^!aeDk@Qnt0+dH3!trKzdihD&cYVQ}fi9pOYAigX7aYBZ8uK|mrKn_q|Q8Pffr&4lEHV+nW9c#&-QOW!FyJV+j<Iu*}*e=sQcK+9;+vP+%sofJn`(+MNyZwG>hd!^5-1dn1eLhmQDR3j;+yKFxb_$%qmbxMh0R)^IsMZqj2Xrkyu7xZ0npG`XLP;*{hX&70dOhyw`Ft-q@F_<71Bkg?s#3tHDmq31?G-)ndd*}g=x#+W0=|Q4;R<jsU>;AkmTHk;5CO-?Ku|^4R8WJi1vS`$7zK2~<07ZS5k=sQp6|4ydY8?&_8i)#IH#e3?+DV-4?CT%p&bAx)NYp}0L`2NhtscWxgZcA6nnj`=ek`e($IiFSPW8voDv*{6&*51G*1<={3S<|Amw7d1(YW{17&h7OBo4*d5Ycbq=5A2ATT;6QnK>2NR2sUA~hzAUL8;pk|C5Dvla-}HLe3|u@`sj3Jd$@;oYFD*s?T<J3*=l+NP}t8z~1Ws-UU>msPi=Dnma<haw*+hf!^ygsAA6K-4b3jcChEHOf#fKxJvyfHn#$bOSm~?(%9x%Jc$AgbT|s-9eCfKk~CLgprPi4!)8Q$=5=s>VW}wG#u77TV_SG9HXIijS;+SjLKl$NbRS)aqpg+arMa4(0FR}@F+f`Z&3i~SnN-{?Kd-GH?lo6k>ZjvD!ha+dr3Luk=K<&v~dz53_<jyDp&(Navj3d*h-lImR9oAt57V4*~KFYvtcN)-^Qx%#d0kBEd~;~cvo&ZHBkyoAQ6};t)5OD>XKI?VKMqC;hDA|0d!JA2n$-CgF=3q92Z@qDVe7z%!AR?WSOG=Nkk8|zl^9T6cM#ciu!=bLufrL99xEd1WEU6htcUGni&h0X~Jllf@MsZ2v$^F!MV)1$UI>;I@P_J2W&=`P)P_+PUslHRIU&UgQIGAmK!dqhQnsV-MH7_#mPTIp{3Z3W*#Ecc1@smi_9X5+bEhQ=w8D3eiS$}vyY%gFQ5?Q=t&Tk#bd*J9OcN#*&KK;PyyZM<biAKuxPf~Hqq|6Ju^#~{>~Re9fLRaq1#2G#jt2&LyET7-$@jWHk95zn1fc-"
"JhN(UNoLS;<M6I<4vSIOL_5Y^=*QTsvKu7tmJubPAS@uQL~<+z$<;h#WKD^tq#H}Rj&W#jP)@9}(<%Ffkq*v@4Aj&qk?9Y-G3g|f{C}mkbf#alOtvS60+<Tp-U<IWdhIJ0LdhIyC9>B+mY!YCh}E>c(TG-H7>hNqnT)Jk#{95z3Ij=WbWMr+;gV3w(F2+*uO#iNeb&fh)_U7P`jrU2h#=_)8Fb8Ajl9Je5M5JVNC$tVYnBWxIY7oLjYkAoq!3XY9yUuhy+Gbz4L5oy>_&+Q1YM$YDP(tHj@QU-Wa#aq3886WA6djBD^DS@hA1nOKdVoc8)rkAeKH!TG|jkV|GJ^?R&s3d)q)p$wnAw>Rz@*9g)Cs1eia~@R~aw%yg;`3&s>%GyBlYe0!%-OyDG8MVBpiHO!HJ-aMOW~DR<?}!c^n5XrF4C6fG*?Bxi6D_6@koC*`t@Q=)C0hB4Vj{vE2DDnB`kBF{#|SB-Amj|ujogp<%bCJw(Gb+eekar+InLRPFFews1iD{GYa%Ik;Xx#<=1q6!9*>$S*h%VPEXNM~+O83hsQZ!d1;8W3=7UQn_Wzgg~Hi1}VmC7$cW(vjO$iGpDvQ*y(gmD~#k^s(M6W)V1Ly4Hwp3iI*g`h)S@luzE@wKv!AlF^pQTrb2+^IKnD?0L~AukRYq^;;Ji6GwpTX9Vz+%L8L=6PV@IGaPV|Gq}jnlFfoKzk~Uyr>5MtEuSi1BcQPmj!{$H#kTq2^}>jql4za`k)!L)h;1_o3`=tKgjQEsyuWXE*adFy8UY)J{LpG@Df7|}sj$&V6!JE?z68m!Fw#Dm+PhL-x%oiHWU?Q4XoigLg%xHb9P(sH(c-m`Gs!-(dL&Vh>=f-|b{TFTYn*h;c&gVw>l^Mabh|3SpKg;eo9z1R6q+@RKdFGXGi3|;vpQx)VO*@40{&c;zXZEy`oLqWXw`0#5JH8XX(&;r$Y}e7$PA{?kMZV7>PHFvu**NAe%yxYI)=$UC2`{>Nns-`##16@x>Jc4lBkCuR%RfTAn}SNVJSdMXhV}&T9Nf0@T7IPHJ9+t!2}G>U<O*Ii4YLXa*Sb|%jNhE`+a3$|F;FKbfgGvEXP;$?1_0k<6<uuiTDCUUJJRIV4nLS>b&^5F@6URpVli^&%sV7?&#Kckbc><A5xs8#TBG-W=2Uwzqi$4WZ&O+AkLyO46%;DUq+C8ScdJDQ)Reu5=;Th9)Tp=N6_+I4akk;B%$1a^+8334|Y1f;GpGz6`(FU;~~%bjKfI3yJt_Fv;mmMsRwM`4q7b8Mu(v9*&S}cB0bO`fiQmssB<GWX(@K5^5XcuX9UY_3<S*IULw+oVO_+il2bIq5XO%6mKILZB-~U~e5&u6kW;o6@<3+C7zLwtqqUG08{}NbRf%M_VR~97Iq)DkAigrZJ1j2hdk~WLUBfYCq<X<w$??^QO?t}jGN!~=hH@l!+sO{jWSv*8D2FXK4qXq8jQ)U;u2FYc6k?6g;bpXK906O*9P1eLPKj4Ye&bI;>96?M9KMC0Oee9vBAz{~?`dz8RwoF!)Re%&h*7cJCYlUmAbfH3{7l$h6V^9Z_KM#E^RZ-PLqs?y++&SEM$-?U=c7KCANaHJ56}*j*d2I$6Q=EZOQ#*cT2s6w(cUS1dGX5egTlF2*tWphchIqf%duQOR=VCkxBisw%s28-Bz_vAy{DfEC`kjtwFlV0JUD*W$-f>th7^|SUCDQk()Z+v>bF@=;wy6T_Fn(ARYp4c!DE>`f{uQhjQAnXuqMQl-4-L_oe}N*78!;0Wh8=Ah_w%RXOWR4XTUgZ00+{dEhfH)u?X9Qa1V$;R<y*$bs_N^q2~Yuh8~f_;zA<F3Dz5pZFDKftfMSavoev)24{V8-L#OMt12=Qm;w2x#U=ZR(`mb8(;R3sNvCb*1?0=EaIjb|gvOn)msmBC@?GjO8gg9bB*#D?=#QQo@cCQM_4^SE1}Nq=10(_SBj&VI;B06)H$X*vl)I#XicoHlYVrFx7DRpiYAt@V0&ZyOQfiGV^#}be"
"Dwm$BxWMlVsNFw`k!Jxhmz!e&z`Ox+O;F%mLjD9Zc}&RDdI4<<Uf?%t;R-IGhgo>53o&Yqif}`r5CV?*s2mqT$D?(Fu62ANi~}l6CjG@uhckMy3wXJ}Wk>aHyMOJuUN_-o3Evwc?}elFT#w5^NB*qQ54)WW<R?JjbOlu{A8H6P61}bGyWJ?VWC;S=Qcbf3&U&X^vbEurmyjrHEP09NIwo0}FARucKb8q{_Rx7j5{57-z#O4=mN}idNvff@LslStsX)2|qF<f@v22V{v_jBwlnCfer_5RlQypZ{-9^zECab@|Zx`CUx^K@l;%sWlYRpBJe#1lhH&!cR<JBw(RHz^-SCv$E3Cp#^d#>q_!+Wk2+?AaIO`RnN(JX`~bqos`B`k83605nJcG*vf+$?fzxeAGQ^cRN3(9c6m{G%!$p<Nfy=_eH&o-t7k-r>E~fUt4!E@2~6Yz%{pT0a>{DMNrqj}d@-XIGPfB+~{MzHOE;VwdSAh%D#}XY*u;6<da$y_Bj<&K@zOl4khUCFd6Z6L0%X&f1DohRhE?9YV@xOcS!Pv~<kb4N~17GG4>TD+V1SffBEf^f)D+Cu^o-Zl&CgM3ye702ei>dyk00BL{U8lqV+m7_GAHl$=G4NEQcdvN+K(Q%t0uL-L!I#)-^C$8=+<;zcr%k_k#$<p3vrvx1V$LLXye7)eZ0J5buo;S_}xVwsLvBY|+bW01nYEQJo4LMRFbg_zS0@|aL)g<OVhyqiwN)7%i+LKn+!FB9z`6GCy4c_KHhFB+(e=o|Fyx-tx1vnr9_8u<?>o1zK!5L04O2sb4Zs64F@Mwk}$QL|T<yyISxf-s<NNYr{|kd}u?VLMa)%1Q*{1o~MApUWibsZh8Ysu#kFq9@9&baR*n#G0EWcq0@J5--eI#YxM?;XT)%K`fY@4xRi!jx?B5>5F6|%L6f6j!4b&@ggan&6RJjwRDv-D7^1|j}7mRuoq-Xg=(ww_Y0{fEDDb@Y%7DiM}o5R1etdll3WUB^&R}a$W5`NB~8#PJA=S%V<qGU9*Lo3Kettwuu5{>&JrB?s|f#InJKZHXTH)>U#$TU;t+q3DaU|RyJXZV^8p$5VZa@v{s|+K^~#t-rd#$_L~%qkmtC{Lv1W3}jOIFX{{Y(Z$PHtzxfBhwToElpq*2o;HG?$O0BZ8F0-hl!7<Bd~3<tlC65t7t2Br#{%9Jt42Sq1Yu(JTnv3&2UkUqbraxtB2knuKhTS7mawUbmRPWssb7_=JWFbv|Ns~n<DIG_9%IY?^*yNCqwHG544M2&=xd}-j-PKAOD4(dmaTr3{)sqiS+LejRErC27No?2wnMNX^GS*2l;2~8DoT#u9^e#-kFkYdHr=5nY@h6{48IBMDa#!49`rxMmw>hrwlx`Q#dgccf40&$h&P+wsj1-$a(DypDd0A=HX59c?5a{Tg6+xLkeS}<cw83gI3EH1+yc^Y}kTzz!i&_`qz%$=I^%f#vO0o>Rzhbrtk8X%}Dpvs~$G`oft9DgNxyu6GCIm2kUlgI$g-i!r|3XD_Pe-^NBrZL6S7R)2H3$`1lAH|RK6BpI>3tW9zztGz=YW?~vR&tV4mLDzIPzkTbnB(HZeHb+3_ORfC2V=<@LyjdY(bP;5l6VdoEk_9Gk8WD{C#qjn@sYl%2}@xtDYMC4p(9PY$bgCCnHfYgQ-IO}nUo+yx7<>OtvY!{IgA1wWg;66kNkJ}o1w418BWd`@)1b=Wckb@zGE0<3f~Fp&!oOiyyf*B;0P0Zu#-t5kI6b+egQMoR%#*7?jT1Q+Q|jPX;k(d)A?dZqfd=|14l`|3mJf;Xk#Bni)Led$VJWg{GVmx(8J_6lIhj6q4y;MrN0RaTS1m%!t&>ZLEmMT%y<yF16Hya?Y#V{A8o19uO3D}8%Y}jQgfX#l^KUpw^)GL=$h?<Mm5_cE0BdfPqxjXH+K1b1DrJGli|jaXomoTY291s$8t#ONn=H_n>b5L0V#|#v^!NKZ+mXaD$`yW8io!Wcgl~>4tr(TDsP$0oK2#B"
"&u9neP^2ooEu?9-%QU-?8fDyz?yf1**`JOXa%g8}Nn96b5Kd~tVvw9JypDdQrm!Zp&p}W|lM@iyH*jCQ+}E}l>T7`<gbw+=8S-wB3!#f-2Nnmx1_zn9X>!>>(Aq0c3MHvWI3W4ktqyq9Mbb(jk8mKIJqKc>-^qki-hYOS7RInnu9hL2+%6A^mP)e(_6Ja~rR<l`|6wm2Qyiz60`k@mKP0R-VO*<;URVANjnMkG0rhQ$gJU-j{TuI#b#A=!1UYaehDF;%#;8yptTk9eoCfrt42<y8D+#rUHo<{?^YG8viJ!hOavY7-LcwvkEk|9;$qLk`<y>EG@~-f)#yI)IvhVI0`Y|u3<GcnUv<_oD!aqqH9hq)~PE7r{Xd0xDrS%~dQcdiusfGm4s(=<n6_kgcQW>YUE+@huaYDhjB1n=Vm0teX&_lc&MQzYzMj9(u+HUTm`OHoC><*J|HE5K>soBCbYD-OtmQo9n(`0Er&c0+C$rJ_jl!?K9%WfiNP%>?uuy2f4Z9fqVokJ7kt70~?ZXA9lgtbm?OU*7ROoD5YlkJENI*YOt^%%0;nVPm_CZX4~%@w9BnOQp3uovjw6^2N{N<j-{%m*n|2|;q?CZT(RyoyscW7fgum3_;Bl+yg89}2%)X6@W@#}<gQwpscEPjk?<*E=JILaWR4r%s}9ywo<4%=Uy2gO^hi=3m!X`)CW6Zk2jBa0z^j{}|$&^*2j#LYx5wx-bR0=;s<N;2ZO2z3*ip2Ta&^%8YOk+oyy5);EE*8Bq*x2`NAaiBFVh%--~77`J!_Q=b{4UCgOqznA#<6-z~=P-s(F0opnRmk0pQxJ5t9fxvRd@H1gTdT(<4(NnUifk#L&Ja8#LvzHL3^bw&v(m3<2Gaqf4Ch{I!{utrAS^)>`-<YOvqCJuO^J(8$?Gge1odk8Bjvp1%4jJ{8#p)T_aq5_$4OE1@B|*+)2UN~t8YMdhL;!=YK%^x^F)uPBA~`0K;}jxZ>;)XTDAPeIVh`pZE1aOXTu217f*gmLun5As#$2Z&BG4;rv>-%<zhCHyrt|9&)^jEATMybv`!HDL<db1Ux-x6Qianj0L)VJ^9{Jm{F#5si<0uin1haL9a<Ra^dgi@E=ze~XU}4BiI;p}Vl>wfn^^ZSG^mXJ|=Vfkk%`I6Hik`P57+QN?C>Uxz@0bu`4Sq8~60iou+ztvn%hsH?go*?yclj|?gmRZILAg+nV@q4lThd_G*U*6KkD&~1=(yvkHHw9f3ALOTqTGg{KYC#(xTKXldWZ!OW0=>wBzi6-70m6Rz_q*uxn^?3v3|-$(9oc3;ldY^>+nMI5MJo>HAK(nBIG~3aM?0{RK<e9CD9AH$p-Ez4>~}xfZ1^s3szy(!0oWFy_DVybE(JK(0ZZA;a_{9*B(0Oynqk6%a`-LK!nTYTzj6+jlkowwO;IXFKa!Q1GoE_DA#h)(qkCKfwdp<c~E5eG6b}2NOjz-OW6&udL#=5o2;-T2f1_*X~1afEzmxPL&AufV2df-Oro$6!mog}-UT(n#kMQYyxLfyEd@6<VS!m@l(~WacCIibKgsnt<Q#-GZLAu~_%&qMVN}AjPm+;wx+G<ymO@^LOa5Bj@CMyr&B$&lvRd}jB`8N#YDDGbxnwy^_U)c)(CDd;4e$A)@EA=01^J*j^?))2SF|X*EvbB#Ipr%TvchLxG*B1OH|X1SWoFf?Awv!iJrWkGzq29g@G?4dN_}+85?^s6j}<eK<!hT7ifHCR)UGDnELT+b>3Vd%W;>NyyQ5}EuJj{^w7{C-+m@WH3;*Et*Fxa+vEf(ljtDp3na2!l4K3T0S2(wJ>nSj2#GD|WFX%&)=9S?tImzW*B+~}?>LHUISIohaq4(hGF|@S9^u2OdgnN;bR}dll<it@X`7>dt>pQ&HOg0fh-!@Qq3jW6;4N&v!u+(8tB<R6ETV;2YGr(|6VH@OYly*W%p=$>{glEW8DT!-}k~F`SsJgOsq#R0gHRN8tUd#YPzN<(8)U%2JxLOE6?W_cVu9kw_d-OE&"
"PQrT1onlc`GDz&fen13<g;R1QOX9F(RG>Gvl_>(lEH_1wrphr;-VyQ2FUbT&?6OaWDFPyz6C5Eem?My#Dnf=MN9eO?gg0D?cxb<Qf_ufuDU}4lQu3foP_oii2~n~?H^WJr9OR@|-a|<!ltfFk<Z}|k<D^?9=~*aBLXtoZU)aN<!jhA$Ia!L8>uotU9Xp96<89P4n=JD|AdF~CF<DN2m8G~>P8WHrAS1uaIQ7Y?B+Ge2{uwVREwYz9eaM&;tK{pUvxw<Vq*<WHE9`d+@3}$I3zHo?YcXH8qLTgXO6sjP1^Z|XsEX(tq)D|k;qg|Nw;y-Qk;eV`!^b^2f86Klare`ZDMOEYPLF$5jhoTMcWzS=KW#+_?F^)~@fl)M>K`-Sak3I3t_^^^^s-1vFZx5tBIjDLW-=Pfadq$OJm#}u!cpNhn%7b?OG&FCndKl*SspaWG2z-W{K`Ect2&+MmpenJ7Q-#H0J_8NY8`BsJNQ7Vl)FAdn80VN5Z|L~Tv)CuN;VLzDWzfr<mg}W;QHHs*NX0?`Jh-SbnJJZAKo2TrvRmVRb9%YzfNnRo>1!SA16t}wiDz1Aua{j08TlZ0*QF#WRu*#<T}}F=V^%08isLZw3GNDdfI`6JR{r+!J8z)>XO|y8oeJgKtE0Z$hj79Z9uIJ<91&A+GRS$<Y!bG8QYjaCREnGqG}OjpC~<NriR@t)dP}Q8hnJ-y`bb>SL*bbPty4{FaUtGBzh%mhGw!g>6yRWD7xNBnq2d2*CYlLCEc%Mss-j<g%1^`#)4%ljjau)D=7bDYIU{TCbKU22~sKja!Mxb@(%JUcx0KLe<_mv?4b9<kn-3~+9E#-BGq|rs-cZL4SJoR+RDTm<8)6s)DE_RWQ!uN8y)Hf3(FYog<(R<Yk1Z1K$)G^+AZ&D5_TdQDZEaB0obFC_6zKmgLYM*nOZ~JTCo59DCYvo-I6{2Qw#*34EptcL)J#fbdbw5iQ%jwt`4Bp6pam~|AcaAOwTKR52*K9@J0zQku<nzZIiQ4<oApC6a%Gm(iAZSN-KkKP_;LqMm((sTvBaw_u3WFG%0JqFBuoGrMK~R1tU|aHB)U|fW_6NB2L*nyaxo#+#3>4on*OAX=7k`kUsfitSqHRd~!PEqb;XiAb~F}1e}B%A0fZZFF_e+4L^+{&8mjCxqM~lW?X(r`hByU3vZD5W+e`rfnbN6Y38lM+3H0DbrF37Zm)#7vhSnT&-Lwzi_>Xa1;liX^>3B%XVxRWsD=una<Ot;WBvcxrk>U{D6@%iR$eS&yYE2EC_6Cb@5${(IdZlvr|1bTNWl^CK$#ZlAoPlUx~C{ZnBrZM_OHuLatF}Wy8&&Xwhs(H#8qF-$IQ-Vv1%!nqZiA(n;!a+6R^4<V`h0JkR^QyC<l&P8G5+kQtSI3R6F_Od?MiCh_G%n=0MD#`Yt|hO>C24lT6Y=M~X>CIeOnga2EIX3hsQ9+zA2svKkhRvDqB38vQFkg;kc5j2A-EB~oLI(Wj`lSrhoA>j$9~Mu~ej7ZRUjpQOsPDqdJT;p}-cqG;e<Qa*7UQOO_(d^^={RH#@$4$?ivw@vgn%RA}*I|*pjvBiTlb%45}FS=v%fp2wbk%{BwcuvmwDo=}}V-|6R+>VRGD1~sj0-8p%yvvwVXwUNEP*!UM-9k8-q00{o5UjXiC6c&+D-u-M8FKn9#<y^|_}+9dZr^esW|eag^tX_r&@5+{6y)?$1FHsYFw;)$2r+2~=q)4PCFximEkmQ!V26zV2Y~B`e`Mv2kilkIIw^^6LFmacwH7?u`PB(#wrhksGP4g0P&s-wXokqNO{N31xPg9&gjvS*(=rw!@<tqVN|Ffr_f8ufrYDXgs|gCi)1g0#L^}%F&`h~OGbM?aT{Wg$J)bGHd`eZB5|YcQnQ{xsw6_&~)UgB2@>g=MS(c;pEEDx4ue<Zsf%V4WJzt|W3X6EA6kd9Dq%f<@{@s7C&QQG>av4m)w$Bz=$a!V|t!shkJna)yB91%y4&Fd(AFoe`go?5Tdnm(?J=CB_"
"i27)Xl{RPRrW{)^rEMVE2Kgkd0J3y638+dfxVcN_jY{+iIuR}<63(6jQCaFD{l_RZQtfim3**lx`|X&OMsQ=XguCdJL%2{PTkZ>_$#@}22dGDUkb!i+2rC_o_9j}mSCcMDyOWcCOi6*BdKq<NEQXBvpsUIWyEM9kC}hmIE1BLlbRk#r&323?>5#f?nrfcNl}Ld~jRj`uuy_y(qL-b8z+cwMN<YF*K9)faMta{xCmP>|-tPmUqLxl9Bp<=T0)!qU-2$2cyA9fvPLgEZmeATsBYTbxLgXqZ70V%Foi>@p7t(&J3(AVcm?QjPjnnwCVU&cQLK&n$=Z~VfGWGI@)LFOu9Z?!YjXGz+Euco)?*pgKDV=aaIrMmSyo5C&ttAzPt~XVzITbQm=V<jL<!B`jBd2D9ZcLK+bV+s4qhxALb1D?}&GZ-{@4Y=vdbq7fM~X;x#pu|_YMCVk8xo@kBtq9HV(|>fF_qGnQC);?fI!f<>&kT1g7@@<{YElVy7+0UYrmLdh5A1l@;Sbe3ay{(!+L8|V{4fSUo2;A``KanCqmg8gyS(jEX)X3{<<~ny}N{!%PTnSV#6{iw=;)5Za!2bKdM}6me2JJJ<O&8%qs5}LmxDifDxshhJ=3lL41%YN6H7(q&)%9(u|TstleXhr&Qu^|0Qh8$N^Fu(D;SV4?h=I7P#cs38`I5r+OgDYV;{NFkYl&Y9>I*_OhU4Qzc4CKkfY>2{NOkR+gjcGOp}0q3nP|VnLGS(2QU~)a_+P7MU5<k9mpV;b%fztP*v9J@g)>!uu2t@v~WEj4H|acRxSVit)9n@xAX?!>pcuxbKy(X=eoR3H|R=;IKg@qPe9ud28S9DANpjl*C${gNcU;gRD*hkwJN=gNHcM%&C4q=cR21O2VumFDOXBO51d-l}Y(64yV;rDO-4eMXP$Ij|n5gtv52QxD{6#QVEDWm!04(3YKchpjOteOVzt#3vDORVGr3EV8h~1>3y<tss;77%j*qFOh7fZL5Mnw<bkqm0v3NHpftZ%?(JY+dX(nLV9m2x{#sJb6fY~Y!gk{@X_l@nL;ohU#vhP7R>&#RHGqN~JxD9pV?}n$S(SK(b7*CSILKe2nB=s+J*-wkyfaNelHVO(R;Yyirptf?L{6S4M>z1AU%$++u0%Sf_~i>c6!jH#pDNHJ2Ln*FW<}RF%)!Uy1P8T(HCVAy`zw?(v&k8L07{rJ#~s7FqqIcH#8qo;B#xBzU@0npZJL5C%}JV88upych<Tqjnp!(U>!KG8KS+GvtK0xFuo%4uz5K3XukaEDw@iuTsAwlbq0QGZQH+~V50eL%UBjfyH559zN(3%87nqxy#;F*K^-Op3G#yAm@k$8w&~sN})r2sisVu5IiOSlB$py|e_@}B}wJB4*CBd5$mFKQh<dzS}f1du6?^xw1<+RAJP4g0HJQY!^#*^X%y6hF!&q?-lwEQzIgSKgp{Mo~2w%kyh#9Bm@@xEUfe4e7d9hE3<oYCLz=846Akc$U_f&#6?bcn$V3TvT<xaJ^tNuwL(wJm^&A}(KzZ2D20U>-~xm7%h{l}z_i9jJ?rfx78LyFq6<=tMw;bi+7qOp}g<%tK(U5&pSZl=X8Sm7%h@hwgQA+q53I%Ibw2tLZ%&nEqTh3Pdp}f+wC{a7Az1N@e-=9d=aVMwbGZh?Y_HR*yoWo<pF=_U!qBcJ1)fx)2SITd!75pKe8iLFLF`|5Hf2UeF`IjFYEmmJYo)%Lkyfw8$`YtTl2XRYno=?ie6BW&RE@{rbp91(CaC9qE9Us@KJ_dFZ*%<X8sl&8P<L=3OM|)tluRbv;2RkLq4t27gP-FGcbNz45M+3u7zYmw9P7e#LRiqvx+!x_s^V%a<*0J^%RSh%H+}K?nhofE|mN&qaZ6<(l(XtUzoj6=^(yicszeD^PCvQjVR_dj1N6EkA~8ITqC)w+u0E=%kaVwG{}KuUOuqnq0Od)Vl82r7L)2AF*Rrw4S%@7{mg>718sKJ!Uz>)}H5eQs7zDa^A9~W^(n3p|!}R"
"U@6zKoRYYsApjViC0G{>9vi*j*d<6VTNaA0TX_OtOP3<HZ0Yjox+NiXTkHA9hL)dm{;@PH6)<c;>==qs;Bz|9`Iyh`ZT*<vy{vVe-x)e*UC_Dw-1C<N2``Np;IT_iSbM(5;a+=w$cMo1wYOdx^q#o(JPv%m<D*<l+X=@JikB`u=fZ{niZrf7pq;g&T2R{6NpPX{52?@V@Eh!u^HM!rU=nps&PjbDhj#UgTEf$6lTu44`5Zygyuy+PG#pUsFYSMkcQCKk*-292#*`o((e78)?M*|X(WIxSdR?M&IGP*(bO2E)fl_Uvx^=f`Uo4<pk<@W|*fFXH)R|GNO6=52p6klc-Qj8_KQxaL$ZWOVSPL=Ud%$Zp_GbpseFl-LUInGiQsd^0GiF^=)#_ibRzJ-*TENPKs;<>ieoeVci*mLK`jJ^`+Po3^h5mGFP$j|DR}S9A*tT8UH~j3Cgi}URC9PC*=5n8TR)#=xmx`0`V>c+xjOAvp>9wcfsM)3N>N#)M3mYRewlG%9t=&<prB<^|nyuA(P}i$kPwRTmBf_fJLUZ+-e+`?b(Q$vI8l|1RDvA;mjalATB$`mTq(fRE6(u#cQ%9Ssb4ecP5gkS0F&za>j~^bbD^Pb^bFH#mwTWuOweHk)Qd5N)eNzpHh8e02vtp7@|6+ic#_NQM{v!hT6W4W2E(Un}I;sHvoTIPfM*>vd;u@>3`Yo=tGhvHgkG7t-ywd2t{QU49CNH~MTT9U@L4u~eRlXx&=`-S(&l%mc&%pYUtJ5p1`e#t;QzG^3P{$*hap+LyWL;DhXxGE))=`s<406ku#>}M2NF+n4JC})N6!q0)VYTa%CNs$cG0jbTz7aA<4$=4#HLbK;^M?fL&qS5tj|lu@v|b1N$RF&Y>BaV+6>ZZeM8<i=3(;d;>{gucnr8d!!aKbCN|TOZ63K+R6?T%AgF4D!D@Pej(N4wFI!fTnbQIue9o0P8S(752H6f4{HE?&GZ0OeDIWyiu&mXEdHR;rG>WPkX2X(wf4;*nd92Hli<hYha<O=S7M^f-V8SwUUl3giw^EiJ(>tLMdS4)&iOtAf|6D57Rh!eaUtP?q)$xmpfL_6eAi`=ggE1`&_NTZ;{a#^+*)D23640!>oGMq@t$5_5_f_7*6&4f=Qo)gq!*i1lap=b4Uf=>BV6OAzPstJvqcaRuYp3INvJ!~yHVpU+d2Ar${$sJ${nNAIyCB07p$vdrpBS~OL0hbsup@H<~BLxfv_%R0pLTC?aAV!<fK!+*KLc*`5*@*HXDj;bB8fdEleN~`P?~N3WJNkwmR;u=OOd0fUA#0(kAXxOF71GmD<?G>PIkN5BBzrDF7FnMrI@}X6lnU>l*TU)r3d-a|`UC>HUp7@YbozCZS_`sbu2E2)ck0E)BI%@#@?;`Ak*n%GV|Lm$;@y7QN|Ti@ST5r2rB$YEhoCrJFZd)g)S1dTHOx;uPv>Gaj|@E<t!gMwRM}>4RR>pk)v1OlhMnpuycjE8tR#~qqV;AN3O``I`MSD=rexMtiD*zMtn}tr{<%&KsIu<w4_a(CA3TcL+*dc7`MTMRzN6WE?WkrmUpJf4y4eizY|^t#viupI%}8xF<F(n0*Jd-UXH)O1@Mn#A&V;?~<*=ygJ*AKt?*h?O?JslkD~X!W?5>%15ryXuYFlbT>s1Q*26;(MGpxIA`Q*S}AnfTn%T-J7cOer<O_~j5)r8s$)ddqXRSBy)?XudCkE~YJI%XuT=N`C>C?JZ?X&@K1d=5I-EkMr(eS*bl9%X4VBVAx0vFxS_YGG6SB23`8X>QL7({=Rpnbmb=*OfxOxk6TMHfzQJEms@n!fd<BFpYeVNfsc0iEoA!!H%a6{9VZMX=tmau9!}lh`L-w9uVT>+xut}v}SY5b=BDTqCj;5=up+?E30ne{|A7YqpJeu|4J;*vFT<Op^$7-LH1^lLhEDW0xH5N9UYEZ*`KK82{^E+Dp;&+#gtj+|8C#VvoW%KYrc;*Ei+d0&V}-oKyrrN+IT6b6@5~X%A^7?!Uj}9"
"p<OJE+)3qP@v>-1vA}Y$YsWB6mT3)8*<LM!FxF_J)+kY3cZc>F!PxH4X<rhJzbajG<h1TT+$UA<tE%^5)%&)pKChtEo9Pp3OBS`xsNr|>2=gwfUTMa9RzcG1D<r?ro!0CiVb0J}2&1+W)K4PACCfD2E_Ifg-f|{8_-!8iG(Qj*ko|P5!BA%l>9quNUL{Jx%Kg<L6J7M0M`|8CoAr=CX%_X&vcRsWGq?Q#9sm$Cwwj+&c$Y#gz<-ZQTx3>O)Q;6`5}j?6_bQ3tB!~ToI^#8EN)kQ;YM$XV6iSm?`(#yRQvI*1lKJ=!b#}GZRatiStCecPw0>um#L=qGARqa{?M<o^8Co4WOk<aQ>X5OGOc5}s=V<=+s?JV1^z5OUeTMD<N*YRQRwlBxM|gWu*&}@Ze6VJBn}#<nW%@?1xu?!!E9u3Qj^*nfb2oL5+o_EXeMW$~nUVZY0jMC|!d+E0O<8m|X%MUQIY!`&&LHQNIzK>yJkDb>7Z``~<ntqPMP>mnWvX)2=C(FHHgsjPIkt>8@AZK7aCmXiqvYw+=wWA<$q9zJrYPs-9|PQGt_O$SGS(~RA5Cql4ykA|x34<1q|_(Z9o6z{sw-PjQ)FHFlv&<cMad%N{n8vrvg$ucy=9D~3NMOk7;_=J)+xnBUpz^iV(1~b2rGa2*f8bj4IA03m&`I|^83`Umw8$sGcqKEFz>r)s%-|BxQ6xvdr7=kAU4TRubdBn<txL_ggRuo%N(eyO8UPC$nh8*Q3B{h-a`lIH|ixJpxdbsw5|blqMHPD7jt!rj}P@SUi(#Dz{Covp23$RECInW6_-?puVtPe`vaLy0aUrh2K6)q6_Ak<1L*!7tCdvO)qO9AwHE!#k3-_qic{6pWWj}7L#OTuFw!i4ua^{k?8u|Xr*|RTHM1q6#6NMSi`LCct)I^-<!Mehidtd%#PdVXU25(fSAO5fr}~}=Q)DF}lOi<Xl_dSEK!wdpqecZO=#0!t(!^JayVzbAsb*CRS8qp!uXBafCTfj}tA}6aZV2a3hxtK7a+R<hmeSi3z{7OtY)Q{_@Sdw2XlK!rqsP`tjMZ6_<V$+PkdDVz>9<tneOfwfKSYJEpJch9FjDj5JB_MC|Bm6I=e|xaJGjFj6>$S=ihNL;c4^u2@hM^DS7J|HIuzH;zsxW4hrLuM@We$XkY4b_GtkW^$=anlY5Wc*5QR;As|j2;Zvwf|cDm(LV1o`5$0QrbTDB4HQV)f!*Ac}kG?zjuQlT>r-|eBjk{W;i{*h18ivqexL7~O1i%+vc=ynkju7F@;ZHZWnl|cs!f-<xJA+qgsWbO|YssC0x`HsFy{2d+<HIwv+W!_<AmJj6}i^-z-X&{424nO>R3Fk#YAfgz95Q#E~l_~<|$Ot4*j*V@Wu@rGt6`n3rKX7T2kyoE0#{hc3;27$%8D?E7M%CLX#w~J;JK@l=Kgd_Cr;|=s_wAxq?k~`T5wtX5xO}=`k~!s6g3#fGC(w)OF3AU{pjcr6c$f_o-i+y>bFC$<?t?&IlIlq$e$|UwJ6U$sWsU#wvi>Xa6IO%G!{qqVj)PLfTox+)9=&U9Iezqy6r`e@VcUgmvZQ{{kp8WMI&(XoVX6Z9KP1&LEIF#ykuHccL;Y_q*-dLh=mUC=B%fs0i^H!4KL$fCK&CJfzrxfAVxnG2kfz>HQzfd}MNQ$T>L4|>q^haZl$V-5^SY_xRJ9&fgkEFHcRn_B!+(Hp|Lds(zmHPGT3PXK=EqsZh<B^wM_uI4J@%VQvM8^BQVcaRG$xKRAsjy)KKSTg3-u_dj0N-wj5ai4{e%(gU~TWXs6M<+6L{cXTeTpQ4+(LRp|;kA?Xy)YDJLgR3$ao-+4AOPV!6S4_oi2wwRh{sf7LhiNR;;vBH}GCT6vm(Ig0xhzXYr9*ZYO`=8Y-u@EDyfMORZK$UwW#vM~gSb~J!#6OdR4VACFeSyr~5k!o|M1TMLm)Zo0fG)goB<-Y*HawEOjRF+sJA-?JjNcHYT+3Du`8o`lJX8QH}2y-M}*>~B7q*bc7"
"CDQXY>XiuOZBqYOLgw3)-IbwXs#j>s8AIvpfvRE8r|Uwdkvmhh^~X%|WUH22>>&3}Qcfqy8qX-F)mR%*7~7=iWRPAvKrBLUm&F*OWGs`<D^3p*c;yxu$7F=*iGrZKR;C+i*hM;M@jlt#My;c#9Tl4#OR8mLDl;bxEK2-lnmJ=i<mL?Oke}zUOHreneI)uhSvwmWL49P9kKdRED|wJ<yi<ICH}f9(AY$aX=p^<JdD+m0f#X!BZGkYhS3g&(%uc&B(d4fB!3x?F!SuVW>N!cX!CkqSQH>@$*>mqvN=!NAWFE@NIjf=fl&6$Nij2I$GXP_uN(TI+yl#d396wbIY&1)L%RBv}66N)oL5Bv^D?6K+29WW$iWeG5y!4vJ_>}p`tfBy~H2n;1(sYj(%rQEvu8x#Ge_`365m6<f25D|n$jURJIyc3kg;%X9^=s!rj2{_b1l#qIsWoa(g-%eBpW+OKb>f_~@-@wAgy&7fQ@snXsNlvvb&izZ1@gP<leM$LTq}9kV>bK&nhtiZ(#jR&ULa{>RG^b19a6ovMP6X;I8G#anE>g1)&xy<nV^rcJJhbWp`&bSg?PaRntMIOxwObq$vbWAqf1q{^>XG(JbH;d@1Y3sm(LG9Oj|iu^=L1!T=e?gZ@f>V#Py$Y)#nCFN4nZR``9o&<l#2AgS3U4cANWN$v0YQm!#zCRQ{<$CMSh7ll7a&B2ChaYEM&I?SQGp?FxPE((sh_Z)NnExPqcG5Rf8K)Aqj5+*dgaVBvKuq8^2&%^Lmi$2MUeGV_1^BsxA=G7n|;Yw1}w0n`K9=o{3#N>AwBu$#?orq|5vF_tY$H<@Rfy7c}5MCIh2+8f_7_ZhMDdk}oO`MCyjJLv;_eIq2S*Y*vOfjZ9>=a;%Nw?5~<Or=1DilIPBd7T2SA=xv*x9w$LJUyVL)OwpyQto-&7EvI2n*oE?s5ekffT{LsCw|qT_m5^|Y7vljYED$W9Wk*8$gfI|nfqjsMF6v=#7gU7R{^gK)8jFIt&iwi${}6HoG3gLUP^18M?GYx9has9Hel+T0Q{2{onJ10J;b+Y&&{mYbWt8>n6E<l#Ph?uui+b)Zyw$it?pO<T9_Q3HzOsU@dxQ$NJ7~K;xt|c%=LKk{rsR~fR3PW?bTzj=9}6kEcEJn+Lh0*W|5U*c~fB#H0Ebbf!>yo(x6ehE>-3oY`U@A6xRbLU+*(b7=A$ry>c&BZCaW~hNl(+Cg!n0lXm==oNUpXR%F41>iC3=vQa%@v-4Qp+|II^Ri|{-jk;==$$CXywYkyd*HzoA$FWa^IHE0aHD7O-6Cl$L-T5&OSq?D3CY8Ul$c7L{CP-jYRxiK9oS*Em(rZ%6*XUD#m7i5Dy-v2t-i-<aJfRtS?LO&t&@-Ajf=;ex;RH+tbm3W7b(=S5Zq$3K6m{z6;UPYU4Eu67@d^2_*}OET%ceYn6*^6{f5`@V!z|$lwGOaJV^xPDd8eBGjRHeTZMsZ3sPC$n(z$H%SBW2ZsqoZX2wF^O&b5%D@<a1rdF5;3WI9x#X=K_Y7EHp$bbXO-`DEY0e_?JKU+@)&|HdF4(=PC;4^tlmXSY?@E}L2OxA3ztKZ70><u)s8rZedBHvYc|DKa(YeHT=+;9H<~i!SobL0=`EV7!Zr^g}JOceQD$E+~mvqPG?4iB)r!82)kSJ(#CEYr?O{%YwzwZz$rmA!X{k+9u4hI4{*+@8MSqUZ8gNw)WA$x4Kw2(j%tS>R!F9@`IaR7D`rQ##&^<zid8Q+rj^9Xk68vg)-Wy{z;U2^soWHCdG?pGB+ve3Oluo(^WO<eJ9;eN}p_3-LQl4uI9IXawq*Vwo*NosKm*v$dn_=Y6XMz0C7++20q#8;^*p>oM@-#Bu3Eah}x^#Tc7lxlXZn#%ETnqs`w54)rMR=!PRawsckUTNwjJbQcmxqYrv_G8AC9{)hm|x;Goj{T4d=1Gs`xSzzO3PXFMej@hxQDaUEdd=lM_&+wgD3O=BMNdA%vRE$b@!;B>BAIRH>cQ9d0fKtRr=-ni5^"
"bDWe{fuD)=^1Au^#b4asBU$4)a@RGWS+14ihXqlue1P9d`nFNBk4g&y8r=YmtegHnBRwHKtKUFe;J2RewD40}{JOge^<qvL!ff=Q?6i(CtXX*sD?;7D_i`;<pQ@SL;MTZZ>H&8mpv?X%oNb;K^)8??vsy%1L^f78d380^+ac&5YOCjMMl?+O0n+LYzBi!GO-<{X>&85z(NO*O0`w0Yu+oKTfh5Z<GtJBt;eYGEk1aDdMFsym2l{_2ECl!j!+`l8IOzY!fu%<k?VIe(FMnoM_Ndnk5F58tg#JHo`oB>uBB*%<`pwt%(f*>W8jek}7EfViT9!%cg_-n6^KFikRe_W-w_wzApD^QR$Z8>4<0^c-Ca<=u_OXr!p*LMruN+K3G}3=3*p4+kiX|*W&hwR+_-4W~Xp7W>W+DWaVv%6g*%a5xg*uEvf;7r2dZ!XOrfP2IA(jiQZ_r-b!x5kAq17~$(SSao_xpjWXT1)ZkxCWR{~xcu24dHQ{41rYEs`*mxT8<~X~28($)`rwopJK1=dL?>6@sPoaN-Bwe`@QxruUq-_M-Pt#=9uvj8hOC>-C=ZshnK+`R-wm=|5(nMD-9u?GT4~ny>Cu(|;HG??OjcsKI>LSD5Q_M5;G3h^o(Z?7s_*H5|r@k;5SW35EW9THdzMeALC}r6&Hcnbni)^SYt!$N!Yf+5zi%-HZNVGym(1(|qHjscrnhGTUVJOsK7P4pdQD){xcXfL*3)!=4?;QC|(<m9-PctZYP+>c7jIr)ag*WdYo8uN~EFmbC}x3T#z0R?jgz_0s_QU^b}$h3aAEl=deoN0dG`CCyjf%IcVs3ZvYqnAvqbCckp(S){o~gi>XF3X{)}&gi=Gy6e~JF}3O1Qs#7_Ut>8nCbJt3)3rwblgg#Xl#{jh{E<du*Z**(tQ@D(e0!KaamJop^KmITX(D<+bv^2n<|96;TOIn~vO&|5<nCAJ$f_MYZB(~ijj1}hK{W|3?o^P+)KXnMGinlY=98D>YGTIB?MTGbEpEO&Q=Kzag-x~9#{X2bHreWkZWniwCZOM1qY~9=uNobXw4-_?Ta7lN&_WY1<*AXOA}swbMVf$Yv3gWnHGY@IF-=Nyom$DqPcqg2ohN6i?~BqiTG2SB){HtXZL8Dy_3^x_AJ}5l5u3H@0v1&_f0arDrf?PWj^2*dPBzzGP~nhueBrFVw^`Kq#Kdv4ta}vITqR8X$EfXNR5{bcvG$HvA606v4bk*n_M3TDStm4Xwegytzqq|`n7t>pk8P74?#tmCtfukLR-xaklT)v2*opI`moir^g?Yfac?h0YREdo@){2wwt0F@kS7tYjdMu6H2>!b2eI`!Z>xQZ<z%lKS9u#%tFr$%TBHma3oKtk(G)BGirccdEA}}9|+)}n-zJ|*q>20n#@T&x<-i$CV=FQ$nTaBQqz|jT3w#9&|<f3&h+WMmXTy#W>j(t%qEsD=YF~9g6`Rnel&gP=?z9@w(PD_hY-J<llI3+Jm^NVuFVSHq+;Q;+zz3!l8!w(MEA7&O7;=Q$nO2*t_g?N4!DCOBYRpk_gx=_6?lQD^<s?R7<7^^SjH|0-F>B(q;SS#c;dr&J>(4whUs7Y2Ih}MOCX5D5X>w0Of1oK8xJ`4qnlzD|-JPeuLhhbdqJRIYbhhu!APUo|#rwRw_^*(nMz17iqtNc(MU86ac8VWiN$5T;brB<lQTD3v}T~(bP+NCG2P8Zex{-v&vOIKA_s8P{Ry+)fnOp{i0kgYGI#vJ*-reObf=KsUSOM{kzul(YlS{G^fnaJUNDMb(O9xnn5gxtQvL6!JnApN2R#=|k6D4NHHYpBt$o7q;6El=&FWEFv3Y6YqXDb`QagB1Vt&cl52aDM<V%v19~tp3i<19APOc_8jtc^=4J!@CJ`9S&Ng)FO2)(&8fhYB{|3sl&#&2qqT6*Wp+_9QTLK(876KWVYXuCiWc#ea#(4h0lcRXmxnFj-tD&r!|f?_&+(NF$D"
)

MAP_B64 = "c-k$>PfNov9Dw2e{v^%TL~S>%GPO;>6+H>vCe{q>)EymyOtCVgLp;szf7HR=({p%(0E!N#Vi=K0hSAGF@M$4EKNcHg&MvXK-T<592~@H!=-}uE>I;hdGxq}`PR3Y4ZP&=j{w?2UYv5#WB4+0;P(K=(hXEdn@`_R_(`O@2u#BI0L9dd}pzJMhNtDS^?+qzem2Qx8b=O_O2XUr-=N($&+<4XC_y3{2`a*VHuja4{w+QFZXma6HHin#>@~1{CTY;8;0W5(<a1iYJ16LRtA^"

CHARSET = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:!?%$'\"-()/·&+–—"
TITLESET = "THE WORLD·"
STYLE_ORDER = ["R12", "R14", "B12", "B15", "B17", "B22", "B30", "T54"]
STYLE_CHARS = {s: (TITLESET if s == "T54" else CHARSET) for s in STYLE_ORDER}

def load_font():
    raw = zlib.decompress(base64.b85decode(FONT_B64))
    pos = 1
    font = {}
    for name in STYLE_ORDER:
        asc, desc, n = raw[pos], raw[pos + 1], raw[pos + 2]
        pos += 3
        chars = STYLE_CHARS[name]
        meta = []
        for i in range(n):
            adv, w, h, xo, yo = raw[pos:pos + 5]
            meta.append((chars[i], adv, w, h, xo - 64, yo - 64))
            pos += 5
        glyphs = {}
        for ch, adv, w, h, xo, yo in meta:
            nbytes = (w * h + 1) // 2
            glyphs[ch] = (adv, w, h, xo, yo, raw[pos:pos + nbytes])
            pos += nbytes
        font[name] = (asc + desc, glyphs)
    return font

FONT = load_font()

def text_w(style, s):
    glyphs = FONT[style][1]
    return sum(glyphs.get(c, glyphs[" "])[0] for c in s)

def draw_text(style, s, x, y, col):
    """Draw s with pen at (x, y); y is the ascender line."""
    glyphs = FONT[style][1]
    pen = x
    r0, g0, b0 = col
    for c in s:
        adv, w, h, xo, yo, data = glyphs.get(c, glyphs[" "])
        gx, gy = pen + xo, y + yo
        for row in range(h):
            py = gy + row
            if py < 0 or py >= H:
                continue
            base = (py * W) * 3
            for cx in range(w):
                idx = row * w + cx
                byte = data[idx >> 1]
                a = (byte >> 4) if idx % 2 == 0 else (byte & 15)
                if a == 0:
                    continue
                px = gx + cx
                if px < 0 or px >= W:
                    continue
                i = base + px * 3
                if a == 15:
                    PX[i], PX[i + 1], PX[i + 2] = r0, g0, b0
                else:
                    PX[i] = (PX[i] * (15 - a) + r0 * a) // 15
                    PX[i + 1] = (PX[i + 1] * (15 - a) + g0 * a) // 15
                    PX[i + 2] = (PX[i + 2] * (15 - a) + b0 * a) // 15
        pen += adv
    return pen - x

def wrap(style, s, maxw):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd) if cur else wd
        if text_w(style, trial) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def draw_block(style, s, x, y, maxw, col, lh, max_lines=99):
    lines = wrap(style, s, maxw)[:max_lines]
    for i, ln in enumerate(lines):
        draw_text(style, ln, x, y + i * lh, col)
    return len(lines)

# ---------------- story data (Tuesday 24 November 2026) ----------------
LEAD_KICKER = "MARKETS · NORTH AMERICA"
LEAD_HEAD = "NVIDIA WHIPLASH: RECORD RALLY UNWINDS IN A DAY"
LEAD_BODY = ("Monday's record surge on Jensen Huang's return as chief executive "
             "— up 31.5%, adding some $952bn — reversed on Tuesday as Nvidia fell "
             "5.9% to $155.38, wiping out $233bn. Chip stocks slid across the "
             "board: Micron dropped 11% and the semiconductor index 7.9%, as a "
             "board investigation and the Dec 3 Senate hearing weighed.")

NUMBERS = [
    ("$290bn", "war compensation Iranian courts demand from the United States"),
    ("23", "people injured in the Villavicencio car bomb; 80+ buildings damaged"),
    ("5 vs 31", "cargo ships through Hormuz on Nov 22 vs the previous weekend"),
]

# (kicker, headline, body)
CARDS = [
    ("SOUTH AMERICA · COLOMBIA", "Car bomb rocks Villavicencio on peace-accord eve",
     "A car bomb outside the Meta governor's office injured 23 and damaged 80+ "
     "buildings; the president blamed FARC-EMC's Medina."),
    ("ASIA · GAZA", "Israeli strikes kill Hamas security chief in Gaza",
     "Airstrikes killed Hamas security chief Naeem Abu Nahel and five others, "
     "including two police officers, medics said."),
    ("EUROPE · UKRAINE", "Russian strike hits Zaporizhzhia apartment block",
     "At least two people were killed and dozens wounded, including four children, "
     "in a strike on a residential building."),
    ("ASIA · STRAIT OF HORMUZ", "Hormuz shipping nearly halts amid mine crisis",
     "Iran's Guard says four tankers struck sea mines, two under US escort. Just 5 "
     "cargo ships passed Nov 22, vs 31 the weekend before."),
    ("EUROPE · ANTALYA, TURKIYE", "COP31 ends with no fossil-fuel deal",
     "Climate talks in Antalya collapsed without a fossil-fuel agreement. Analysts "
     "say the failure lays bare a divided world order."),
    ("ASIA · MYANMAR", "14 nations back ICJ genocide finding on Rohingya",
     "Fourteen countries, including the UK, Spain, Canada and Australia, affirmed "
     "the ICJ finding of genocide against the Rohingya."),
    ("AFRICA · DR CONGO", "Ebola teams trapped by fighting in Ituri",
     "Heavy fighting near an Ituri hospital disrupted Ebola response work; teams "
     "took cover for over 24 hours, the WHO said."),
    ("AFRICA · LIBYA", "UN seeks probe into Benghazi port attacks",
     "The UN mission called for an independent investigation into attacks at "
     "Benghazi port and on Russian vessels offshore."),
    ("ASIA · INDONESIA", "Banten factory fire: 34 workers still missing",
     "Rescue teams continued recovering victims of the deadly candy-factory fire "
     "in Banten, with 34 workers still unaccounted for."),
    ("NORTH AMERICA · USA", "US sanctions Iran exchange networks",
     "The Treasury sanctioned more than two dozen Iranian exchange houses and "
     "front firms under 'Operation Economic Outcast'."),
    ("ASIA · WEST BANK", "Israeli leaders denounce settler arson attacks",
     "Political leaders condemned 'Jewish terrorism' after settler arson attacks; "
     "Eisenkot joined the condemnation."),
    ("ASIA · PAKISTAN", "Lahore chokes as AQI crosses 500",
     "Lahore again topped the global pollution ranking as AQI crossed 500; eight "
     "Pakistani cities were among the world's worst."),
]

BRIEFS = [
    "Ukraine strikes oil sites in Tatarstan, Perm and Rostov, Russian officials say.",
    "Magnitude 5.6 earthquake strikes Nepal's Koshi province, near the Chinese border.",
    "Iraq's PM orders the federal oil ministry to take over Kurdish-held oilfields.",
    "Seven countries urge the EU to limit Russian travellers' entry, even for sport.",
    "Germany first to gain access to Ukraine's Delta battlefield system.",
    "South Korea offers $375,000 rewards to catch AI cheating in entrance exams.",
    "Bolsonaro rushed to intensive care in Brasilia with acute bowel obstruction.",
    "South Africa's first female deputy president, Phumzile Mlambo-Ngcuka, has died.",
    "Supercell storm devastates Brazil's Tupancireta, displacing thousands.",
]

SPORT = "SPORT · CRICKET — Pant's 128 in Wellington: Asian wicketkeeper record."

# one map marker per story: (lon, lat)
MARKERS = [
    (-122.0, 37.0), (-73.6, 4.1), (34.3, 31.4), (35.2, 47.8), (56.3, 26.6),
    (30.7, 36.9), (95.9, 21.9), (29.4, 1.6), (20.1, 32.1), (106.1, -6.7),
    (-77.0, 38.9), (35.2, 31.9), (74.3, 31.5), (49.2, 55.8), (87.1, 26.9),
    (44.4, 33.3), (4.4, 50.9), (13.4, 52.5), (127.0, 37.4), (-47.9, -15.8),
    (28.2, -26.2), (-53.9, -29.1), (174.8, -41.3),
]

# ---------------- layout ----------------
MX = 28            # left margin
RX = 996           # right edge

def right_text(style, s, y, col, x_end=RX):
    draw_text(style, s, x_end - text_w(style, s), y, col)

def draw_map(x, y, w, h):
    rect(x, y, w, h, MAPBG)
    raw = zlib.decompress(base64.b85decode(MAP_B64))
    pos = 0
    for r in range(41):
        n = raw[pos]; pos += 1
        py = y + (r * h) // 41
        for _ in range(n):
            s, ln = raw[pos], raw[pos + 1]; pos += 2
            for cx in range(s, s + ln):
                rect(x + (cx * w) // 112, py, 3, 2, MAPDOT)
    for lon, lat in MARKERS:
        mx = x + int((lon + 180) / 360 * w)
        my = y + int((90 - lat) / 180 * h)
        rect(mx - 2, my - 2, 5, 5, RED)
        rect(mx - 1, my - 1, 3, 3, WHITE)
        rect(mx, my, 1, 1, RED)

def masthead():
    hline(MX, 8, RX - MX, INK, 3)
    hline(MX, 14, RX - MX, INK, 1)
    draw_text("B12", "GLOBAL EDITION · EST. 2026", MX, 30, GREY)
    right_text("B12", "ONE PAGE · 23 STORIES", 30, GREY)
    tw = text_w("T54", "THE WORLD")
    draw_text("T54", "THE WORLD", (W - tw) // 2, 18, NAVY)
    draw_text("B12", "TUESDAY 24 NOVEMBER 2026", MX, 82, INK)
    right_text("R12", "SIX CONTINENTS · ONE PAGE", 82, GREY)
    hline(MX, 96, RX - MX, NAVY, 2)

def lead_and_rail():
    draw_text("B12", LEAD_KICKER, MX, 108, RED)
    draw_block("B30", LEAD_HEAD, MX, 126, 588, INK, FONT["B30"][0], 3)
    draw_block("R14", LEAD_BODY, MX, 206, 588, INK, FONT["R14"][0] + 3, 7)
    draw_text("B12", "THE DAY MAPPED · ONE MARKER PER STORY", MX, 330, NAVY)
    draw_map(MX, 348, 588, 92)
    vline(628, 108, 332, LINEC)
    draw_text("B15", "BY THE NUMBERS", 640, 108, NAVY)
    hline(640, 130, RX - 640, LINEC)
    y = 140
    for fig, label in NUMBERS:
        draw_text("B22", fig, 640, y, RED)
        draw_block("R12", label, 640, y + 28, RX - 640, GREY, FONT["R12"][0] + 2, 3)
        y += 76
    hline(640, y + 2, RX - 640, LINEC)
    draw_text("B12", "SIX CONTINENTS", 640, y + 12, NAVY)
    draw_block("R12", "North America · South America · Europe · Asia · Africa · Oceania",
               640, y + 28, RX - 640, GREY, FONT["R12"][0] + 2, 3)
    hline(MX, 446, RX - MX, INK, 2)

def cards():
    for i, (kick, head, body) in enumerate(CARDS):
        cx = MX + (i % 3) * 326
        cy = 458 + (i // 3) * 104
        rect(cx, cy, 314, 98, CARD)
        hline(cx, cy, 314, LINEC); hline(cx, cy + 97, 314, LINEC)
        vline(cx, cy, 98, LINEC); vline(cx + 313, cy, 98, LINEC)
        draw_text("B12", kick, cx + 10, cy + 6, NAVY)
        draw_block("B15", head, cx + 10, cy + 22, 294, INK, FONT["B15"][0] + 1, 2)
        draw_block("R12", body, cx + 10, cy + 56, 294, INK, 13, 3)

def briefs_and_sport():
    rect(MX, 882, RX - MX, 96, NAVY)
    for i, b in enumerate(BRIEFS):
        bx = MX + 12 + (i % 3) * 322
        by = 888 + (i // 3) * 30
        draw_block("R12", b, bx, by, 300, WHITE, 13, 2)
    draw_text("B15", SPORT, MX, 988, INK)
    right_text("R12", "THE WORLD · 24 NOVEMBER 2026", 990, GREY)
    hline(MX, 1014, RX - MX, INK, 2)

def main():
    masthead()
    lead_and_rail()
    cards()
    briefs_and_sport()
    out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR") or ".", "entry.png")
    save_png(out)

if __name__ == "__main__":
    main()
