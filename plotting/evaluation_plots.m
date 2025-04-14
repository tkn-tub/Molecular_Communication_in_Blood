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
colors = {'#f34859','#6f4688','#5db6e7'};
lines = {'-s','-*','-*'};
lines = {':o',':s',':*','-o','-s','-*','-o','-s','-*'};
dist_full_lines = {'-diamond','-o','-s','-*'};
dist_dash_lines = {':diamond',':o',':s',':*'};
color_offset = {0,1};
y_bounds = [-5,34];

%%% create evaluation collection structures %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

exp_type = ["blood", "glyc", "water"];
exp_inj = ["90degree","0degree"];
exp_dist = ["5cm","10cm","15cm","20cm"];
exp_velo = ["7,5cms","15cms"];

max_type = size(exp_type,2);
max_inj = size(exp_inj,2);
max_dist = size(exp_dist,2);
max_velo = size(exp_velo,2);
max_entries = 299;

times = zeros(max_type,max_inj,max_dist,max_velo,max_entries);
data = zeros(max_type,max_inj,max_dist,max_velo,max_entries);
theory = zeros(max_type,max_inj,max_dist,max_velo,max_entries);

%%% load the evaluation data %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% load results data
P = '.././data/plotting/';

for t = 1:max_type
    for i = 1:max_inj
        for d = 1:max_dist
            for v = 1:max_velo
                result_file_name = strcat(P,exp_type(t),'_',exp_inj(i),'_',exp_dist(d),'_',exp_velo(v),'.csv');
                if exist(result_file_name, 'file')
                    result_data = readmatrix(result_file_name);
                    times(t,i,d,v,:) = result_data(:,1);
                    data(t,i,d,v,:) = result_data(:,2);
                    theory(t,i,d,v,:) = result_data(:,3);
                end
            end
        end
    end
end

%% plot blood over changing distance at 90° injection and 7.5cm/s
figure;
hold on;
time_points = zeros(max_entries,1);
data_points = zeros(max_entries,1);
theory_points = zeros(max_entries,1);
for t = 1:1
    for i = 1:1
        for d = 1:max_dist
            for v = 1:1
                c_idx = (t - 1) * max_dist + d;
                l_str = exp_dist(d);
                time_points(:,1) = times(t,i,d,v,:);
                data_points(:,1) = data(t,i,d,v,:);
                theory_points(:,1) = theory(t,i,d,v,:);
                plot(time_points(:,1),data_points(:,1), dist_full_lines{d}, 'Color', single_colors{c_idx}, ...
                    'DisplayName', strcat(l_str, ' data') ,'LineWidth',2.5', ...
                    'MarkerIndices',1:20:length(data_points), 'MarkerSize',10)
                plot(time_points(:,1),theory_points(:,1), dist_dash_lines{d}, 'Color', single_colors{c_idx}, ...
                    'DisplayName', strcat(l_str, ' theory') ,'LineWidth',2.5, ...
                    'MarkerIndices',1:20:length(data_points), 'MarkerSize',10)
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
legend({['Measurements, $d = 5 \:\mathrm{cm}$'], ['Fitted Model, $d = 5 \:\mathrm{cm}$'], ['Measurements, $d = 10 \:\mathrm{cm}$'], ...
    ['Fitted Model, $d = 10 \:\mathrm{cm}$'], ['Measurements, $d = 15 \:\mathrm{cm}$'], ['Fitted Model, $d = 15 \:\mathrm{cm}$'], ...
    ['Measurements, $d = 20 \:\mathrm{cm}$'], ['Fitted Model, $d = 20 \:\mathrm{cm}$']},...
    'Location','northeast','NumColumns',2,'Interpreter',"latex",'FontSize',legendfontsize)
legend boxoff;

%% plot blood VS bloodsub VS water for 5cm and 15cm at 90° injection and 7.5cm/s
figure;
hold on;
time_points = zeros(max_entries,1);
data_points = zeros(max_entries,1);
theory_points = zeros(max_entries,1);
for d = 1:2:3
    for i = 1:1
        for t = 1:max_type
            for v = 1:1
                c_idx = t;%(t - 1) * max_dist + d;
                l_idx = (d - 1) * 3 + t;
                l_str = strcat(exp_type(t),', ',exp_dist(d));
                time_points(:,1) = times(t,i,d,v,:);
                data_points(:,1) = data(t,i,d,v,:);
                theory_points(:,1) = theory(t,i,d,v,:);
                plot(time_points(:,1),data_points(:,1), lines{l_idx}, 'Color', colors{c_idx}, ...
                    'DisplayName', l_str,'LineWidth',2.5,'MarkerIndices',1:20:length(data_points), ...
                    'MarkerSize',10)
                %plot(time_points(:,1),theory_points(:,1), '-', 'Color', colors{c_idx}, 'DisplayName', strcat(l_str, ' theory') ,'LineWidth',1.5)
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
legend({['Blood, $d = 5 \:\mathrm{cm}$'], ['Blood Substitute, $d = 5 \:\mathrm{cm}$'], ['Water, $d = 5 \:\mathrm{cm}$'], ['Blood, $d = 15 \:\mathrm{cm}$'], ['Blood Substitute, $d = 15 \:\mathrm{cm}$'], ['Water, $d = 15 \:\mathrm{cm}$']},...
    'Location','northeast','NumColumns',2,'Interpreter',"latex",'FontSize',legendfontsize)
legend boxoff;

%% plot blood VS bloodsub VS water for 5cm at 90° injection and 7.5cm/s and 15cm/s
figure;
hold on;
time_points = zeros(max_entries,1);
data_points = zeros(max_entries,1);
theory_points = zeros(max_entries,1);
for v = 1:max_velo
    for i = 1:1
        for d = 1:1
            for t = 1:max_type
                c_idx = t;%(t - 1) * max_dist + v + color_offset{v};                
                l_idx = (v - 1) * 3 + t;
                l_str = strcat(exp_type(t),', ',exp_dist(d));
                time_points(:,1) = times(t,i,d,v,:);
                data_points(:,1) = data(t,i,d,v,:);
                theory_points(:,1) = theory(t,i,d,v,:);
                plot(time_points(:,1),data_points(:,1), lines{l_idx}, 'Color', colors{c_idx}, ...
                    'DisplayName', l_str,'LineWidth',2.5,'MarkerIndices',1:20:length(data_points), ...
                    'MarkerSize',10)
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
legend({['Blood, $v_{\mathrm{max}} = 7.5\:\frac{\mathrm{cm}}{\mathrm{s}}$'], ['Blood Substitute, $v_{\mathrm{max}} = 7.5 \:\frac{\mathrm{cm}}{\mathrm{s}}$'], ['Water, $v_{\mathrm{max}} = 7.5 \:\frac{\mathrm{cm}}{\mathrm{s}}$'], ['Blood, $v_{\mathrm{max}} = 15 \:\frac{\mathrm{cm}}{\mathrm{s}}$'], ['Blood Substitute, $v_{\mathrm{max}} = 15 \:\frac{\mathrm{cm}}{\mathrm{s}}$'], ['Water, $v_{\mathrm{max}} = 15 \:\frac{\mathrm{cm}}{\mathrm{s}}$']},...
    'Location','northeast','NumColumns',2,'Interpreter',"latex",'FontSize',legendfontsize)
legend boxoff;

%% plot blood VS bloodsub VS water for 5cm at 0° injection and 90° injection and 7.5cm/s
figure;
hold on;
time_points = zeros(max_entries,1);
data_points = zeros(max_entries,1);
theory_points = zeros(max_entries,1);
for i = 1:max_inj
    for d = 1:1
        for v = 1:1
            for t = 1:max_type
                c_idx = t%(t - 1) * max_dist + i + color_offset{i};
                l_idx = (i - 1) * 3 + t;
                l_str = strcat(exp_type(t),', ',exp_dist(d));
                time_points(:,1) = times(t,i,d,v,:);
                data_points(:,1) = data(t,i,d,v,:);
                theory_points(:,1) = theory(t,i,d,v,:);
                plot(time_points(:,1),data_points(:,1), lines{l_idx}, 'Color', colors{c_idx}, ...
                    'DisplayName', l_str,'LineWidth',2.5, 'MarkerIndices',1:20:length(data_points), ...
                    'MarkerSize',10)
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
legend({['Blood, 90$^{\circ}$ Injection'], ['Blood Substitute, 90$^{\circ}$ Injection'], ['Water, 90$^{\circ}$ Injection'], ['Blood, 0$^{\circ}$ Injection'], ['Blood Substitute, 0$^{\circ}$ Injection'], ['Water, 0$^{\circ}$ Injection']},...
    'Location','northeast','NumColumns',2,'Interpreter',"latex",'FontSize',legendfontsize)
% legendflex({['Blood, 90$^{\circ}$ Injection'], ['Blood, 0$^{\circ}$ Injection'], ['Blood Substitute, 90$^{\circ}$ Injection'], ['Blood Substitute, 0$^{\circ}$ Injection'], ['Water, 90$^{\circ}$ Injection'], ['Water, 0$^{\circ}$ Injection']},...
%      'anchor', [3 3], 'buffer', [-10 -10],'ncol',2, 'nrow', 4, 'Interpreter',"latex",'FontSize',legendfontsize)
legend boxoff;