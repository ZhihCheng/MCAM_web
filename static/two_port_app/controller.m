% Step 1: 打開 Simulink 模型
scriptPath = mfilename('fullpath');
[scriptDir, ~, ~] = fileparts(scriptPath);
cd(scriptDir);
load_system('controller_class');

assignin('base', 'wcw_i', 2*pi*f_i);
assignin('base', 'wn_v', 2*pi*f_v);


set_param(['controller_class/Current Controller ', Current,'-Type'], 'Position', [365,191,525,284]);
set_param(['controller_class/Velocity Controller ', Velocity,'-Type'],'Position',[660 211 820 304]);

Current1 = sprintf('Current Controller %s-Type/1', Current);
Current2 = sprintf('Current Controller %s-Type/2', Current);
Velocity1 = sprintf('Velocity Controller %s-Type/1', Velocity);
Velocity2 = sprintf('Velocity Controller %s-Type/2', Velocity);

add_line('controller_class',Current1,'Power Stage/2','autorouting','on')
add_line('controller_class',Velocity1,Current2,'autorouting','on') 
add_line('controller_class','Electrical Part/1',Current1,'autorouting','on')
add_line('controller_class','Mechanical Part/1',Velocity1,'autorouting','on')
add_line('controller_class','Command/1',Velocity2,'autorouting','on')
add_line('controller_class','Mechanical Part/1','Wm/1','autorouting','on')

switch Current
    case 'PI'
        Ki_i_value = 2*pi*f_i*R;   % pi
        Kp_i_value = 2*pi*f_i*L;
        % to workspace
        assignin('base', 'Kp_i', Kp_i_value);
        assignin('base', 'Ki_i', Ki_i_value);
        % app.CKpEditField.Value = Kp_i_value;
        % app.CKiEditField.Value = Ki_i_value;
    case 'IP'
        Ki_i_value = 2*pi*f_i^2*L; % ip
        Kp_i_value = 2*zeta_i*2*pi*f_i*L-R;
        % to workspace
        assignin('base', 'Kp_i', Kp_i_value);
        assignin('base', 'Ki_i', Ki_i_value);
        % app.CKpEditField.Value = Kp_i_value;
        % app.CKiEditField.Value = Ki_i_value;
end


switch Velocity
    case 'PI'
        Kp_w_value = 2*pi*f_v^2*Bm/Kt;
        Ki_w_value = 2*pi*f_v*J/Kt;
        % to workspace
        assignin('base', 'Kp_w', Kp_w_value);
        assignin('base', 'Ki_w', Ki_w_value);
        % app.VKpEditField.Value = Kp_w_value;
        % app.VKiEditField.Value = Ki_w_value;
    case 'IP'
        Kp_w_value = (2*zeta_v*2*pi*f_v*J-Bm)/Kt;
        Ki_w_value = J*2*pi*f_v^2/Kt;
        assignin('base', 'Kp_w', Kp_w_value);
        assignin('base', 'Ki_w', Ki_w_value);
        % app.VKpEditField.Value = Kp_w_value;
        % app.VKiEditField.Value = Ki_w_value;
        % app.VKpEditField.Value = Kd_w_value;
    case 'PID'
        Ki_w_value = (2*pi*f_v)^2*J/Kt;
        Kp_w_value = 2*pi*f_v*J/Kt;
        Kd_w_value = J/(2*pi*f_v*Kt);
        % Kd_w_value = (J*2*pi*f_v*2*zeta_v-Bm)/Kt;
        assignin('base', 'Kp_w', Kp_w_value);
        assignin('base', 'Ki_w', Ki_w_value);
        assignin('base', 'Kd_w', Kd_w_value);
        % app.VKpEditField.Value = Kp_w_value;
        % app.VKiEditField.Value = Ki_w_value;
        % app.VKdEditField.Value = Kd_w_value;

    % case 'Robust IP'
    %     H2opt_I(app);
    %     assignin("base",'K_A',app.A_K);
    %     assignin("base",'K1_B',app.B_K(:,1));
    %     assignin("base",'K2_B',app.B_K(:,2));
    %     assignin("base",'K_C',app.C_K);  
end

assignin('base', 'StopTime', num2str(StopTime));

% Step 3: 匯出圖像
print('-scontroller_class', '-dpng', 'controller_class.png');


simOut = sim('controller_class');

% 獲取日誌信號

logsout = simOut.get('logsout');

signal1 = logsout{1};
time1 = signal1.Values.Time;
data1 = signal1.Values.Data;

signal2 = logsout{2};
time2 = signal2.Values.Time;
data2 = signal2.Values.Data;

% 將數據轉換為表格格式
T1 = table(time1, data1, 'VariableNames', {'Time', 'Data'});
T2 = table(time2, data2, 'VariableNames', {'Time', 'Data'});

% 指定 Excel 文件名
filename = 'simulink_output.xlsx';

% 將數據寫入 Excel 文件的不同分頁
writetable(T1, filename, 'Sheet', 'Signal1');
writetable(T2, filename, 'Sheet', 'Signal2');