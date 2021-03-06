function [SaR50,bRSa,SaT50,bTSa]=SPO2IDAfragility(idac, dry,drlim,buthd,mf,T,Gamma,g,N)
% Estimate fragility parameters for an MDOF system approximated by an equivalent
% SDOF and using SPO2IDA by Vamvatsikos & Cornell (2005).
%____________________________________________________________________________
% INPUT
% Cy     : base shear coefficient at yield (presently covered by Gamma and dry)
%          Cy = Say/g = Vy/W, where Say=Sa @ yield, Vy = base shear @ yield
% drlim  : median roof displacement value that defines the fragility. It can result 
%          from any EDP but it should be expressed in terms of the (median)
%          corresponding roof disp (just like we always do in pushovers anyway)
% dry    : roof yield displacement
% buthd  : dispersion (std of log data) characterizing the lognormal
%          distribution of "limit-state roof drift capacity" around drlim
% mc,a,ac,r,mf : the backbone shape parameters for SPO2IDA 
% T      : ESDOF period (sec)
% Gamma  : the participation factor for the roof displacement(>1) 
% g      : the value of "g" in units compatible with T and drlim, dy.
%          The default is 9.81m/s2, assuming that dy and drlim are in meters.
% N      : Number of realizations to use for Monte Carlo when buthd>0 to
%          incorporate extra uncertainty due to a non-deterministic drlim
%          threshold 
% OUTPUT
% SaR50  : the median Sa for the fragility, in units of "g", considering only
%           record-to-record variability
% bRSa   : the dispersion due to record-to-record variability (i.e. demand only)
% SaR50  : the median Sa for the fragility, in units of "g", considering both
%          capacity and demand dispersions
% bTSa   : the total dispersion, including capacity and demand dispersions.
%_____________________________________________________________________________
%
% CREATED 11/June/2014 by D.Vamvatsikos
% 

plotflag=1;

% limiting ductility that defines fragility
mlim=min(drlim/dry,mf)
% Assume lognormal and do some Monte Carlo
if buthd>0
   xp=linspace( 1./(2*N),1-1./(2*N), N);
   musample=logninv(xp,log(mlim),buthd);
   musample(musample>mf)=mf;
else
    musample = ones(1,N)*mlim;
end

if plotflag
   figure(1);clf;hold on
end

for j=1:3
   [x,indx]=unique(idac(j).m);
   y=idac(j).r(indx);
   rM(j)=interp1(x,y,mlim);
   %if buthd>0
      rMC(j,:)=interp1(x,y,musample);
   %end
   if plotflag
      plot(x,y,'b-')
      plot(musample,rMC(j,:),'ro')
   end
end
      
Say=4*pi^2*dry./(g*Gamma.*T.^2);
SaR50=rM(2)*Say;
bRSa=0.5*(log(rM(1))-log(rM(3)));

% these are simple estimates of relatively good accuracy
%SaT50_0=median(rMC(2,:))*Say;
%bTSa_0=sqrt(bRSa^2+std(log(rMC(2,:)))^2);

Sai=zeros(1,N*N);
% this is to compute the better estimate, still it is much different from above
% estimates (at least for most cases that I have tried).
if buthd>0
   allSa50=rMC(2,:)*Say;
   allbSa50=0.5*(log(rMC(1,:))-log(rMC(3,:)));
   for i=1:N
      Sai((i-1)*N+1:i*N)=logninv(xp,log(allSa50(i)),allbSa50(i))
   end
   SaT50=median(Sai);
   bTSa=std(log(Sai));
else
    SaT50 = SaR50;
    bTSa = bRSa;
end




