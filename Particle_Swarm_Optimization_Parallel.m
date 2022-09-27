%%
% INPUT VARIABLES
% Bird_in_swarm=Number of particle=agents=candidate
% Number_of_quality_in_Bird=Number of Variable
%
% MinMaxRange: jx2 matrix; jth row contains minimum and maximum values of the jth variable
% say you have a variable N1 
% which can have maximum value M1 and minimum value m1
% then your matrix will be [m1 M1] 
% for more:
% [m1 M1; m2 M2; mj Mj]
%
% Food_availability=Objective function with one input variable (for more than one variable you may use array)
% example for two variable
% function f = funfunc(array)
%     a=array(1);
%     b=array(2);
%     f = a+b ;
% end
% Food_availability is a string, for above example : 'funfunc'
%
% availability_type is string 'min' or 'max' to check depending upon need to minimize or maximize the Food_availability
% velocity_clamping_factor (normally 2)
% cognitive_constant=c1=individual learning rate (normally 2)
% social_constant=c2=social parameter (normally 2)
% normally C1+C2>=4
%
% Inertia_weight=At the beginning of the search procedure, diversification is heavily weighted, while intensification is heavily weighted at the end of the search procedure.
% Min_Inertia_weight=min of inertia weight (normally 0.4)
% Max_Inertia_weight=max of inertia weight (normally 0.9)
% max_iteration=how many times readjust the position of the flock/swarm of birds its quest for food
% 
%
% OUTPUT VARIABLE
% optimised_parameters : Optimal parameters
%%
function [ optimised_parameters ] = Particle_Swarm_Optimization_Parallel (Bird_in_swarm, Number_of_quality_in_Bird, MinMaxRange, Food_availability, availability_type, velocity_clamping_factor, cognitive_constant, social_constant, Min_Inertia_weight, Max_Inertia_weight, max_iteration, formula, log_file)
%{
    Checking all functions are present
%}
if (exist ('MinMaxCheck.m')==0)
    clc;
    fprintf ('Please download the following submission from: <a href="http://www.mathworks.com/matlabcentral/fileexchange/43251-bound-values-of-an-array">MATLAB File Exchange (Click here to open link)</a> \ndownload code by clicking "Download Submission" button \nthen extract and put MinMaxCheck.m in current directory and try again\n');
    return;
end
%{
    Checking all parameteres are entered
%}
if nargin < 12
    error('Missing input parameter(s)!')
end


%{
	universalize availability type  
%}
availability_type=lower(availability_type(1:3));

%{
	 Checking for proper boundary Values and entered Matrix
%}
[row,col]=size(MinMaxRange);
if row~=Number_of_quality_in_Bird || col~=2
    error('Not a proper MinMaxRange Matrix')
end
for i=1:Number_of_quality_in_Bird
    if MinMaxRange(i,1)>=MinMaxRange(i,2)
        error('Minimum value greater than Maximum value!!!')
    end
end

%{
	 counter to display % of completion
%}
N=Bird_in_swarm*max_iteration;
q=0;

%{
	 distinguishing min and max range
%}
bird_min_range=MinMaxRange(:,1);
bird_max_range=MinMaxRange(:,2);

%{
	 
%}
format long;
for i=1:Number_of_quality_in_Bird
    bird(:,i)=bird_min_range(i)+(bird_max_range(i)-bird_min_range(i))*rand(Bird_in_swarm,1);
end

Vmax=abs(bird_max_range)*velocity_clamping_factor;
Vmin=-Vmax;
%Vmin=bird_min_range*velocity_clamping_factor;

for i=1:Number_of_quality_in_Bird
    Velocity(:,i)=Vmin(i)+(Vmax(i)-Vmin(i))*rand(Bird_in_swarm,1);
end

oldCount=10;
err=inf;
gBest=inf;
for i=1:oldCount
    gOld{i}=inf;
end
itr=0;
while err > 1e-2 && itr<max_iteration
    fid = fopen(log_file, 'a');
    fprintf(fid,'Completed  %d  %% ... \n', uint8(q*100/N ));
    
    itr=itr+1
    fprintf(fid, 'iteration: %d \n', itr);
    fclose(fid);
    for i=1:oldCount-1
        gOld{i}=gOld{i+1};
    end
    gOld{oldCount}=gBest;
    tic
    parfor p=1:Bird_in_swarm
        parameter=bird(p,:,itr)
        availability(p,itr)=feval(Food_availability,parameter,formula,false);
    end
    itrTime=toc;
    fid=fopen(log_file,'a');
    fprintf(fid,'Simulation time for iteration %d: %f \n',itr,itrTime);
    fclose(fid);
    for p=1:Bird_in_swarm
        switch availability_type
            case 'min'
                format long;
                [pBest_availability,index]=min(availability(p,:));
                pBest=bird(p,:,index);
                
                if(p==1 && itr==1)
                    gBest=pBest;
                    gBest_availability=pBest_availability;
                elseif availability(p,itr)<gBest_availability
                    gBest_availability=availability(p,itr);
                    gBest=bird(p,:,itr);
                end
                
            case 'max'
                format long;
                [pBest_availability,index]=max(availability(p,:));
                pBest=bird(p,:,index);
                
                if(p==1 && itr==1)
                    gBest=pBest;
                    gBest_availability=pBest_availability;
                elseif availability(p,itr)>gBest_availability
                    gBest_availability=availability(p,itr);
                    gBest=bird(p,:,itr);
                end
                
            otherwise
                error('availability_type mismatch')
        end
        
        w(itr)=((max_iteration - itr)*(Max_Inertia_weight - Min_Inertia_weight))/(max_iteration-1) + Min_Inertia_weight;
        Velocity(p,:,(itr+1))=w(itr)*Velocity(p,:,itr) + social_constant*rand(1,Number_of_quality_in_Bird).*(gBest-bird(p,:,itr)) + cognitive_constant*rand(1,Number_of_quality_in_Bird).*(pBest-bird(p,:,itr));
        Velocity(p,:,(itr+1))=MinMaxCheck(Vmin, Vmax, Velocity(p,:,(itr+1)));
        
        bird(p,:,(itr+1))= bird(p,:,itr) + Velocity(p,:,(itr+1));
        bird(p,:,(itr+1))=MinMaxCheck(bird_min_range, bird_max_range, bird(p,:,(itr+1)));
        q=q+1;
    end
    
    gBest
%    disp(gBest(2))
%    disp(gBest_availability)
    fid = fopen(log_file, 'a');
    fprintf(fid,'Optimal parameters until now: \n');
%    for i=1:Number_of_quality_in_Bird
%        if i==1
%            value1 = 'Dm_K';
%            value2 = num2str(floor(gBest(i)));
%        elseif i==2
%            value1 = 'Dm_Na';
%            value2 = num2str(floor(gBest(i)));
%        elseif i==3
%            value1 = 'Dm_Cl';
%            value2 = num2str(floor(gBest(i)));
%        else i==4
%            value1 = 'gap junction surface area';
%            value2 = num2str(floor(gBest(i)));
%        end
%        fprintf(fid, 'Parameter %s = %s \n', value1, value2);
%    end

    for i=1:Number_of_quality_in_Bird
        if i==1
            value1 = 'Dm_K';
            value2 = num2str(floor(gBest(i)));
        else
            value1 = 'Dm_Na';
            value2 = num2str(floor(gBest(i))); 
        end
        fprintf(fid, 'Parameter %s = %s \n', value1, value2);
    end

    fprintf(fid, 'Optimal score until now: %f \n',gBest_availability);
    for i=1:oldCount
        ERR{i}=norm(gBest-gOld{i});
    end
    err=max(cell2mat(ERR))
    fprintf(fid,'err = %f \n',err);
    fprintf('\n\n');
    fclose(fid);
    % clc;
end
optimised_parameters=gBest
fid = fopen(log_file, 'a');
fprintf(fid,'Final optimal parameters: \n');
%for i=1:Number_of_quality_in_Bird
%    if i==1
%        value1 = 'Dm_K';
%        value2 = num2str(floor(optimised_parameters(i)));
%    elseif i==2
%        value1 = 'Dm_Na';
%        value2 = num2str(floor(optimised_parameters(i)));
%    elseif i==3
%        value1 = 'Dm_Cl';
%        value2 = num2str(floor(optimised_parameters(i)));
%    else i==4
%        value1 = 'gap junction surface area';
%        value2 = num2str(floor(optimised_parameters(i)));
%    end
%    fprintf(fid, 'Parameter %s = %s \n', value1, value2);
%end

for i=1:Number_of_quality_in_Bird
    if i==1
        value1 = 'Dm_K';
        value2 = num2str(floor(optimised_parameters(i)));
    else
        value1 = 'Dm_Na';
        value2 = num2str(floor(optimised_parameters(i)));        
    end
    fprintf(fid, 'Parameter %s = %s \n', value1, value2);
end

fprintf(fid, 'Final optimal score: %f \n',gBest_availability);
fprintf('\n\n');
fclose(fid);
% close parallel pool
% if ~isempty(gcp('nocreate'))
%     delete(poolobj)
% end
