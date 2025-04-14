%%% workspace %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc;
clear all;
close all;

addpath('./../data/plotting/');

%% Figures

paper_figs = true;

% plot layout
fontsize=20;%fontsize value
legendfontsize=17;%fontsize value
set(groot,'defaultfigureposition',[400, 250, 1000, 400])

single_colors = {'#b00c1c','#f34859','#f88e99','#fab7be','#6f4688','#a078b9','#bea3cf','#d4c2df','#145c84','#1e8fcc','#5db6e7','#96d0f0'};
colors = {'#f34859','#6f4688','#5db6e7','#878787'};
lines = {'-s','-*','-*'};
lines = {':o',':s',':*','-o','-s','-*','-o','-s','-*'};
model_lines = {':diamond','--o','-.s'};
color_offset = {0,1};
y_bounds = [-1,19];


%%% create evaluation collection structures %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

exp_model = ["own", "huang", "yue"]
exp_type = ["blood"];
exp_inj = ["90degree"];
exp_dist = ["5cm","10cm","15cm","20cm"];
exp_velo = ["7,5cms"];

max_type = size(exp_type,2);
max_inj = size(exp_inj,2);
max_dist = size(exp_dist,2);
max_velo = size(exp_velo,2);
max_entries = 299;

times = zeros(3,max_type,max_inj,max_dist,max_velo,max_entries);
data = zeros(3,max_type,max_inj,max_dist,max_velo,max_entries);
theory = zeros(3,max_type,max_inj,max_dist,max_velo,max_entries);

%%% load the evaluation data %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% load results data
% our results
P = '.././data/plotting/';

for t = 1:max_type
    for i = 1:max_inj
        for d = 1:max_dist
            for v = 1:max_velo
                result_file_name = strcat(P,exp_type(t),'_',exp_inj(i),'_',exp_dist(d),'_',exp_velo(v),'.csv');
                if exist(result_file_name, 'file')
                    result_data = readmatrix(result_file_name);
                    times(1,t,i,d,v,:) = result_data(:,1);
                    data(1,t,i,d,v,:) = result_data(:,2);
                    theory(1,t,i,d,v,:) = result_data(:,3);
                end
            end
        end
    end
end

% Huang results
P = '.././data/plotting/_huang_';

for t = 1:max_type
    for i = 1:max_inj
        for d = 1:max_dist
            for v = 1:max_velo
                result_file_name = strcat(P,exp_type(t),'_',exp_inj(i),'_',exp_dist(d),'_',exp_velo(v),'.csv');
                if exist(result_file_name, 'file')
                    result_data = readmatrix(result_file_name);
                    times(2,t,i,d,v,:) = result_data(:,1);
                    data(2,t,i,d,v,:) = result_data(:,2);
                    theory(2,t,i,d,v,:) = result_data(:,3);
                end
            end
        end
    end
end

% Yue results
P = '.././data/plotting/_yue_';

for t = 1:max_type
    for i = 1:max_inj
        for d = 1:max_dist
            for v = 1:max_velo
                result_file_name = strcat(P,exp_type(t),'_',exp_inj(i),'_',exp_dist(d),'_',exp_velo(v),'.csv');
                if exist(result_file_name, 'file')
                    result_data = readmatrix(result_file_name);
                    times(3,t,i,d,v,:) = result_data(:,1);
                    data(3,t,i,d,v,:) = result_data(:,2);
                    theory(3,t,i,d,v,:) = result_data(:,3);
                end
            end
        end
    end
end


%% plot blood over 10cm distance at 90° injection and 7.5cm/s
figure;
hold on;
time_points = zeros(max_entries,1);
data_points = zeros(max_entries,1);
theory_points = zeros(max_entries,1);
for m = 1:3
    for t = 1:1
        for i = 1:1
            for d = 2:2
                for v = 1:1
                    c_idx = (t - 1) * max_dist + d;
                    l_str = exp_dist(d);
                    time_points(:,1) = times(m,t,i,d,v,:);
                    data_points(:,1) = data(m,t,i,d,v,:);
                    theory_points(:,1) = theory(m,t,i,d,v,:);
                    if m == 1
                        plot(time_points(:,1),data_points(:,1), '-', 'Color', colors{4}, ...
                            'DisplayName', strcat(l_str, ' data') ,'LineWidth',2.5', ...
                            'MarkerIndices',1:20:length(data_points), 'MarkerSize',10)
                    end
                    plot(time_points(:,1),theory_points(:,1), model_lines{m}, 'Color', colors{m}, ...
                        'DisplayName', strcat(l_str, ' theory') ,'LineWidth',2.5, ...
                        'MarkerIndices',1:20:length(data_points), 'MarkerSize',10)
                end
            end
        end
    end
end

box off
axis tight
xaxisproperties= get(gca, 'XAxis');
xaxisproperties.TickLabelInterpreter = 'latex'; % latex for x-axis
yaxisproperties= get(gca, 'YAxis');
yaxisproperties.TickLabelInterpreter = 'latex'; % latex for y-axis
ylim(y_bounds)
set(gca, 'YGrid', 'on', 'XGrid', 'on')
set(gca,'linewidth',2)
%set(gca, 'YScale', 'log');
set(gca,'FontSize',fontsize);
xlabel('Time [s]','interpreter','latex');
ylabel('Frequency Shift [Hz]','interpreter','latex');
legend({['Measurements'], ['Our Fitted Model'], ['Fitted Model, Huang et al. [10]'], ['Fitted Model, Yue et al. [20]']},...
    'Location','northeast','NumColumns',1,'Interpreter',"latex",'FontSize',legendfontsize)
legend boxoff;
