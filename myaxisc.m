classdef myaxisc < handle
    %MYAXISC Multiple axis class containing multiple axes systems
    %   H = MYAXISC(N,DY) creates multpile empty cartesian axis object H
    %   with N (two ore more) independend y-axis and one common x-axis. N
    %   is a number of y-axis to display, DY specifies the spacing between
    %   the outside axis lines as relative size of figure (between 0...1).
    %   H is a handle to the created maxis-object, providing methods to
    %   change appearance and properties and holding all the axes-object
    %   which are used. All axes-objects are created with "hold on", so
    %   scaling needs to be done after plotting into the axes.
    %
    %   Usage:
    %
    %   H = MYAXISC(2) creates a dual-axis object.
    %
    %   H = MYAXISC(5,0.09) creates 5 axis with spacing of 0.09
    %
    %   H = MYAXISC(parent,2) creates a dual-axis object in specified
    %   parent container
    %
    %   H = MYAXISC(5,0.09,[0.1,0.1,0.8,0.8]) creates 5 axis with spacing
    %   of 0.09 and outer position of [0.1,0.1,0.8,0.8] in current figure
    %
    %   H = MYAXISC(parent,5,0.09) creates 5 axis with spacing of 0.09 in
    %   specified parent container
    %
    %   H = MYAXISC(parent,2,'app') creates a dual-axis object in specified
    %   parent container in App Designer compatibility mode (zooming and
    %   panning as well as axestoolbars deactivated
    %
    %   H = MYAXISC(parent,5,0.09,'app') creates 5 axis with spacing of
    %   0.09 in specified parent container and App Designer compatibility
    %   mode
    %
    %   H = MYAXISC(parent,5,0.09,[0.1,0.1,0.8,0.8],'app') creates 5 axis
    %   with spacing of 0.09 and specified position in App Designer
    %   compatibility mode into specified parent container.
    %
    %   First and second axis use the same axes object for plotting and
    %   outside ruler display. Axes three and up use an axes object to hold
    %   the line plot and a separate axes object to display the axis ruler.
    %
    %   There are some buit-in methods to change the axis behaviour the
    %   easy way after the object H of class MYAXISC has been created:
    %
    %   H.AUTOSCALE automatically scale all Y axis
    %
    %   H.AUTOY(NR) autoscale Y axis number NR
    %
    %   H.GRIDON displays grid, H.GRIDOFF hides grid
    %
    %   H.POSITION([LEFT,BOTTOM,WIDTH,HEIGHT],DY) Change the position of
    %   the myaxisc axis system using a vector similar to axes properties
    %   position and additionally specifiying DY for space between y axis
    %   lines.
    %
    %   H.XLIM([xmin,xmax]) Change x axis limits
    %
    %   H.YLIM(NR,[ymin,ymax]) Change y axis limits of axis NR
    %
    %   H.XLABEL(STRING) Add or change X-Label
    %
    %   H.YLABEL(NR,STRING) Add or change an Y-Label to y axis NR
    %
    %   H.YCOLOR(NR,COLOR) Change y axis and font color for yaxis NR
    %
    %   H.FONTSIZE(S) Change the font size of all text at once
    %
    %   H.CLA Removes all Plots from all axes.
    %
    %   All axes objects containing the lines are stored in property
    %   AXPLT, while all axes objects used to display the y axis ruler are
    %   stored in AXDSP. Therefore, AXDSP(1) and AXDSP(2) are not in use.
    %   These properties can be returned by methods H.L and H.P, while L(2)
    %   will return the same as H.P(2) because AXDSP(2) does not exist.
    %
    %   H.P(NR) Returns handle to axes object used for plotting
    %
    %   H.L(NR) Returns handle to outside axes object used for ruler line
    %   display. If NR is 1 or 2, it will return the same object as H.P(NR)
    %
    %   Additional Methods for App Designer: H.app_***

    %   Version 1.5 by Viktor Hartung, 01. Feb 2019
    %   Published on Matlab FileExchange under BSD-Licence
    
    properties (Access = public)
        n     % Number of axes displayed
        dy    % Distance between y-Lines in px
        ax_p  % Primary Axes
        ax_s  % Secondary Axes (invisible)
        axplt % Additional (invisible) Axes for line plots 3 and up
        axdsp % Additional Outside Axes for rulser display
        axui  % Invisible Axes object for user interaction (zooming etc)
        ylbl  % Y-Label-Objects, if created
        xlbl  % X-Label-Object
        uiz   % Zoom Enabled on user interaction axes (logical)
        uip   % Pan Enabled on user interaction axes (logical)
    end
    
    properties (Access = private)
        xlimpre       % relative x limits before zoom/pan operation
        xlimpost      % relative x limits after zoom/pan operation
        ylimpre       % relative y limits before zoom/pan operation
        ylimpost      % relative y limits after zoom/pan operation
        isOctave      % Determine if Octave or Matlab is used (logical)
        isAppDesigner % Determine if used in App Designer (logical)
        prevlims      % Matrix with previous limits (App Designer Zoom)
        limstored     % Previous limits are stored (logical)
        limsrestored  % Previous limits were restored (logical)
    end
    
    methods % public methods
        function obj = myaxisc(varargin)
            %MYMAXISC Construct an instance of this class
            %   The constructor creates all the desired axes and sets some
            %   properties to the created axes objects.
            
            % Initial values for positions
            px = 0.13; % Axes system X position (matlab default)
            hx = 0.775; % Axes system width (matlab default)
            py = 0.11; % Axes system Y position (matlab default)
            hy = 0.815; % Axes system height (matlab default)
            
            % Process Inputs
            obj.isAppDesigner = false; % if not set
            if nargin == 1 % myaxisc(2) for two Y-Axis
                n = varargin{1};
                dy = 0;
                parspecified = false;
            elseif nargin == 2
                if isnumeric(varargin{1}) % myaxisc(4,0.8)
                    n = varargin{1};
                    dy = varargin{2};
                    parspecified = false;
                else % myaxisc(parent,2)
                    par = varargin{1};
                    n = varargin{2};
                    parspecified = true;
                    dy = 0;
                end
            elseif nargin == 3 % myaxisc(parent,4,0.4)
                if ~ischar(varargin{3}) && size(varargin{3},2)==1
                    par = varargin{1};
                    n = varargin{2};
                    dy = varargin{3};
                    parspecified = true;
                elseif ischar(varargin{3}) % myaxisc(parent,2,'app');
                    par = varargin{1};
                    n = varargin{2};
                    dy = 0;
                    parspecified = true;
                    obj.isAppDesigner = strcmp(varargin{3},'app');
                elseif (~ischar(varargin{3}) && size(varargin{3},2)==4)
                    % myaxisc(4,0.4,[0.1,0.1,0.9,0.9])
                    n = varargin{1};
                    dy = varargin{2};
                    parspecified = false;
                    px = varargin{3}(1); % Axes system X position
                    hx = varargin{3}(3); % Axes system width 
                    py = varargin{3}(2); % Axes system Y position
                    hy = varargin{3}(4); % Axes system height 
                else
                    error('Unsupportet Inputs');
                end
            elseif nargin == 4
                if ischar(varargin{4}) % myaxisc(parent,4,0.4,'app')
                    par = varargin{1};
                    n = varargin{2};
                    dy = varargin{3};
                    parspecified = true;
                    obj.isAppDesigner = strcmp(varargin{4},'app');
                elseif size(varargin{4},2) == 4
                    % myaxisc(parent,4,0.4,[x0,y0,dx,dy])
                    par = varargin{1};
                    n = varargin{2};
                    dy = varargin{3};
                    parspecified = true;
                    obj.isAppDesigner = false;
                    px = varargin{4}(1); % Axes system X position
                    hx = varargin{4}(3); % Axes system width 
                    py = varargin{4}(2); % Axes system Y position
                    hy = varargin{4}(4); % Axes system height
                end
            elseif nargin == 5 % myaxisc(parent,4,0.4,[x0,y0,dx,dy],'app')
                    par = varargin{1};
                    n = varargin{2};
                    dy = varargin{3};
                    parspecified = true;
                    obj.isAppDesigner = strcmp(varargin{5},'app');
                    px = varargin{4}(1); % Axes system X position
                    hx = varargin{4}(3); % Axes system width 
                    py = varargin{4}(2); % Axes system Y position
                    hy = varargin{4}(4); % Axes system height 
            else
                error('Wrong number of input arguments.');
            end
            
            % Some more initial checks
            if (n <= 1)
                error('This class is designed for a minimum of two axes.')
            end % if
            
            if (n*dy >= hx) && (n >= 2)
                error('Too many axes or too much spacing between them');
            end % if
            
            % Check if this is run under MATLAB or OCTAVE
            obj.isOctave = exist('OCTAVE_VERSION', 'builtin') ~= 0;
            if obj.isOctave
                parspecified = false; % There is no support for this in oct
            end
            
            % Assign some object properties
            obj.n = n;
            obj.dy = dy;
            
            % Pre-initialisation, this is needed for zooming functionality
            obj.xlimpre = [0,1];
            obj.ylimpre = [0,1];
            obj.uiz = false;
            obj.uip = false;
            obj.limstored = false;
            obj.limsrestored = false;
            
            w = hx-(obj.n-2)*obj.dy; % Remaining width of plot-box
            
            % Create Primary axes without any modifications
            if parspecified
                obj.ax_p = axes(par);
            else
                obj.ax_p = axes();
            end
            
            % Position primary axes
            set(obj.ax_p,'Position',...
                [px+(obj.n-2)*obj.dy,py,w,hy])
            hold(obj.ax_p,'on');
            
            % Create Secondary axes on the right side, similar to plotyy
            if parspecified
                obj.ax_s = axes(par);
            else
                obj.ax_s = axes();
            end
            set(obj.ax_s,'Box','off',...
                'YAxisLocation','right','Color','none',...
                'XTickMode','manual','XTick',[],...
                'Position',[px+(obj.n-2)*obj.dy,py,w,hy]);
            if ~obj.isOctave
                set(obj.ax_s,'XColor','none')
            end
            
            hold(obj.ax_s,'on');
            
            % Create more axes on the left side: One for plotting, one for
            % displaying the axes on the outside. Link axes y pairs
            for idx = 1:obj.n-2
                % Create Axes to contain the plots and make it invisible
                if parspecified
                    obj.axplt(idx) = axes(par);
                else
                    obj.axplt(idx) = axes();
                end
                % Make it practically invisible
                set(obj.axplt(idx),'Box','off','Hittest','off',...
                    'Color','none',...
                    'XTickMode','manual','XTick',[],...
                    'YTickMode','manual','YTick',[]);
                if ~obj.isOctave
                    set(obj.axplt(idx),'XColor','none','YColor','none');
                end
                % Position where plots will appear is always the same
                set(obj.axplt(idx),'Position',...
                    [px+(obj.n-2)*obj.dy,py,w,hy]);
                
                hold(obj.axplt(idx),'on');
                
                % Create an additional for ruler display only
                if parspecified
                    obj.axdsp(idx) = axes(par);
                else
                    obj.axdsp(idx) = axes();
                end
                % Hide everything except y Axis:
                set(obj.axdsp(idx),'Box','off','Hittest','on',...
                    'YAxisLocation','left','Color','none',...
                    'XTickMode','manual','XTick',[]);
                if ~obj.isOctave
                    set(obj.axdsp(idx),'XColor','none');
                else % Set Color to parent background color
                    % parhandle = get(obj.ax_p,'Parent');
                    parcol = get(get(obj.ax_p,'Parent'),'Color');
                    set(obj.axdsp(idx),'XColor',parcol);
                end
                % Position it according to idx and number of total axes
                set(obj.axdsp(idx),'Position',...
                    [px+(obj.n-idx-2)*obj.dy,py,obj.dy./4,hy]);
            end % for
            
            % Link all X-Axis to enable Zooming and so on for all axes
            if obj.n == 2
                linkaxes([obj.ax_p,obj.ax_s],'x')
            else
                linkaxes([obj.ax_p,obj.ax_s,obj.axplt],'x');
            end
            
            % Link outside display-axes with plot-y-axes
            for idx = 1:obj.n-2
                linkaxes([obj.axplt(idx),obj.axdsp(idx)],'y')
            end
            
            % Implement some Zoom-Thingy to enable zooming on all axes
            % This is neither supported by app designer nor octave.
            if ~obj.isOctave && ~obj.isAppDesigner
                % Add a "user interaction" axes to catch all zooming
                % operations. other axes will be resized according to this
                % one by using some fancy listener with callbacks
                if parspecified  %create axes
                    obj.axui = axes(par);
                else
                    obj.axui = axes();
                end
                % Position it over the plot box containing lines
                set(obj.axui,'Position',[px+(obj.n-2)*obj.dy,py,w,hy]);
                % Make it invisible, but not by using visble=no
                 set(obj.axui,'Box','off','Color','none',...
                     'XTickMode','manual','XTick',[],...
                     'YTickMode','manual','YTick',[],...
                     'XColor','none','YColor','none');
                % Add a listener which observes the axis range and calls
                % a funtion to resize y or x positions
                addlistener(obj.axui,'YLim','PostSet',...
                    @(src,event)axuiylimPostSetCallback(obj,src,event));
                
                % Disable panning by default as this may behave strange
                pan(obj.axui,'off');
                
                % Remove all the default axes toolbars from the visible
                % plots and the ruler displays
                if ~verLessThan('matlab','9.4')
                    set(obj.ax_p,'Toolbar',[]);
                    set(obj.ax_s,'Toolbar',[]);
                    for idx = 1:obj.n-2
                        set(obj.axplt(idx),'Toolbar',[]);
                        set(obj.axdsp(idx),'Toolbar',[]);
                    end % for
                    
                    % Also remove the default axes toolbar for axui-plot
                    set(obj.axui,'Toolbar',[]);
                    
                    % Create a new axes toolbar with zoom in and out btns
                    % as child of obj.axui
                    axtb = axtoolbar(obj.axui,{'pan','zoomin','zoomout'});
                    % Create a new push-button in this toolbar
                    restorebtn = axtoolbarbtn(axtb,'push');
                    % Use matlab default icon for restore view and assign a
                    % custom callback function which will reset the axui
                    % scaling, therefore triggering the listener.
                    set(restorebtn,'Icon','restoreview',...
                        'Tooltip','Reset Zoom','ButtonPushedFcn',...
                        @(src,event)restorebtnCallback(obj,src,event));
                    set(axtb,'Visible','on'); % Always display buttons
                end % if ~verLessThan('matlab','9.4') 
            end % if ~obj.isOctave && ~obj.isAppDesigner
            
            % Implement Zoom and Pan on all Axis in App-Designer by using
            % the primary axes system for user interactions now.
            if obj.isAppDesigner
                % Add a Listener to observe Y-Limits of primary axis
                addlistener(obj.ax_p,'YLim','PreSet',...
                    @(src,event)axPylimPreSetCallback(obj,src,event));
                addlistener(obj.ax_p,'YLim','PostSet',...
                    @(src,event)axPylimPostSetCallback(obj,src,event));
            end
        end % constructor
        
        function axobj = p(obj,nr)
            %P Returns reference to axes object where the plot will be put
            %into. Call plot(h.p(4),x,y) to plot into y-axis 4.
            if (nr == 1)
                axobj = obj.ax_p;
            elseif (nr == 2)
                axobj = obj.ax_s;
            else
                axobj = obj.axplt(nr-2);
            end
        end % function get_paxesg
        
        function axobj = l(obj,nr)
            %L Returns axes obj used for line display only on left side
            % This can be used to set most of the Y-Axis properties.
            if (nr == 1)
                axobj = obj.ax_p;
            elseif (nr == 2)
                axobj = obj.ax_s;
            else
                axobj = obj.axdsp(nr-2);
            end
        end % function get_paxes
        
        function xlim(obj,lim)
            %XLIM sets x axes limits to lim, where lim is [xmin,xmax]
            set(obj.ax_p,'XLim',lim);
            if obj.isOctave % Axes linking is buggy in octave, workaround:
                set(obj.ax_s,'XLim',lim);
                if obj.n >= 3
                    for idx = 1:obj.n-2
                        set(obj.axplt(idx),'XLim',lim);
                    end % for
                end
            end %if
            if obj.isAppDesigner
                obj.storelims; % Store Limits for Restore-Button
            end
        end % function xlim
        
        function ylim(obj,nr,lim)
            %YLIM set Y Limit
            if (nr == 1)
                set(obj.ax_p,'YLim',lim);
            elseif (nr == 2)
                set(obj.ax_s,'YLim',lim);
            else
                set(obj.axplt(nr-2),'YLim',lim);
            end
            if obj.isAppDesigner
                obj.storelims; % Store Limits for Restore-Button
            end
        end % function ylim
        
        function autoscale(obj)
            %AUTOSCALE do the y and x axis scaling
            if ~obj.isOctave
                obj.zoomrestore;
            end
            axis(obj.ax_p,'auto y');
            axis(obj.ax_s,'auto y');
            if obj.n >= 3
                for idx = 1:obj.n-2
                    axis(obj.axplt(idx),'auto y');
                end %for
            end
            if obj.isAppDesigner
                obj.storelims; % Store Limits for Restore-Button
            end
        end
        
        function autoy(obj,nr)
            %AUTOY autoscale y axis nr
            if (nr == 1)
                axis(obj.ax_p,'auto y');
            elseif (nr == 2)
                axis(obj.ax_s,'auto y');
            else
                axis(obj.axplt(nr-2),'auto y');
            end
            if obj.isAppDesigner
                obj.storelims; % Store Limits for Restore-Button
            end
        end
        
        function xlabel(obj,xlblstr)
            %XLABEL Puts an X-Label to axis 1
            obj.xlbl = xlabel(obj.ax_p,xlblstr);
        end % function xlabel
        
        function ylabel(obj,nr,ylblstr)
            %YLABEL Puts an Y-Label to the specified axis.
            %    h.YLABEL(nr,ylblstr) puts ylblstr to axis nr.
            if (nr == 1)
                obj.ylbl(nr) = ylabel(obj.ax_p,ylblstr);
            elseif (nr == 2)
                obj.ylbl(nr) = ylabel(obj.ax_s,ylblstr);
            else
                obj.ylbl(nr) = ylabel(obj.axdsp(nr-2),ylblstr);
            end % if
        end % function ylabel
        
        function ycolor(obj,nr,col)
            %YCOLOR Change color of Y-axes line, ticks and numbers
            if (nr == 1)
                set(obj.ax_p,'YColor',col);
                if nr == 1 % Reset Grid
                    set(obj.ax_p,'GridAlpha',1,...
                        'GridColor',[0.8,0.8,0.8],'GridColorMode','manual');
                end
            elseif (nr == 2)
                set(obj.ax_s,'YColor',col);
            else
                set(obj.axdsp(nr-2),'YColor',col);
            end
        end % function ycolor
        
        function gridon(obj)
            %GRIDON show grid
            grid(obj.ax_p,'on');
            set(obj.ax_p,'GridAlpha',1,...
                'GridColor',[0.8,0.8,0.8],'GridColorMode','manual');
        end
        
        function gridoff(obj)
            %GRIDOFF disable grid
            grid(obj.ax_p,'off');
        end
        
        function axobj = legendtarget(obj)
            %LEGENDTARGET returns axes object for legend
            if obj.isOctave || obj.isAppDesigner
                axobj = obj.ax_p;
            else
                axobj = obj.axui; % Use top layered axui for legend
            end
        end
        
        function fontsize(obj,s)
            %FONTSIZE Changes font size of all labels and so on to S
            set(obj.ax_p,'FontSize',s);
            set(obj.ax_s,'FontSize',s);
            if (obj.n >= 3)
                for idx = 1:obj.n-2
                    set(obj.axdsp(idx),'FontSize',s);
                end % for
            end % if
            if obj.isOctave % Workaround to modify Label sizes in octave
                for idx = 1:obj.n
                    try
                        set(obj.ylbl(idx),'FontSize',s)
                    catch
                        % do nothing
                    end
                end
                try
                    set(obj.xlbl,'FontSize',s)
                catch
                    % do nothing
                end
            end
        end
        
        function position(obj,pos,dy)
            %POSITION Reposition the whole axes thing
            obj.dy = dy; % Set new dy-spacing as obj properties
            
            % Get Values for position
            px = pos(1); % Axes system X position
            hx = pos(3); % Axes system width
            py = pos(2); % Axes system Y position
            hy = pos(4); % Axes system height
            
            w = hx-(obj.n-2)*obj.dy; % Remaining width of plot-box
            % Primary Axis
            set(obj.ax_p,'Position',[px+(obj.n-2)*obj.dy,py,w,hy])
            % Secondary Axis
            set(obj.ax_s,'Position',[px+(obj.n-2)*obj.dy,py,w,hy]);
            % Resize third axis and up, both display and plot axis
            for idx = 1:obj.n-2
                set(obj.axplt(idx),'Position',...
                    [px+(obj.n-2)*obj.dy,py,w,hy]);
                set(obj.axdsp(idx),'Position',...
                    [px+(obj.n-idx-2)*obj.dy,py,obj.dy./4,hy]);
            end % for
            if ~obj.isOctave && ~obj.isAppDesigner
                % Resize invisible user-interaction axis
                set(obj.axui,'Position',[px+(obj.n-2)*obj.dy,py,w,hy]);
            end
        end % function position
        
        function cla(obj)
            %CLA clears all plots from all axis and restores zoom
            cla(obj.ax_p);
            set(obj.ax_p,'XLim',[0,1]);
            cla(obj.ax_s);
            set(obj.ax_s,'XLim',[0,1]);
            if (obj.n >= 3)
                for idx = 1:obj.n-2
                    cla(obj.axplt(idx));
                    set(obj.axplt(idx),'XLim',[0,1]);
                end
            end % if
            obj.autoscale; % Call autoscale
        end
        
        function app_enpan(obj)
            %APP_PAN Enables Panning in App Designer
            zoom(obj.ax_p,'off')
            pan(obj.ax_p,'on')
            obj.uiz = false;
            obj.uip = true;
            % Save previous limits to restore them later
            % Save previous limits to restore them later
            if ~obj.limstored || obj.limsrestored
               obj.storelims;
            end % if
        end
        
        function app_enzoom(obj)
            %APP_ZOOM Enables Zooming in App Designer
            pan(obj.ax_p,'off')
            zoom(obj.ax_p,'on')
            obj.uiz = true;
            obj.uip = false;
            % Save previous limits to restore them later
            if ~obj.limstored || obj.limsrestored
               obj.storelims;
            end % if
        end % function
        
        function app_dispz(obj)
            %APP_DISPZ Disables both Panning and Zooming in App Designer
            pan(obj.ax_p,'off')
            zoom(obj.ax_p,'off')
            obj.uiz = false;
            obj.uip = false;
        end % function
        
        function app_restore(obj)
            %APP_RESTORE Restore All Limits to values before zoom/pan
            if obj.limstored
                set(obj.ax_p,'XLim',obj.prevlims(1,:));
                set(obj.ax_p,'YLim',obj.prevlims(2,:));
                set(obj.ax_s,'YLim',obj.prevlims(3,:));
                if (obj.n >= 3) % for axes 3 and up
                    for idx = 3:obj.n
                        set(obj.axplt(idx-2),'YLim',obj.prevlims(idx+1,:));
                    end
                end
                obj.limsrestored = true;
            end % if
        end % function
             
        function zoomrestore(obj)
            %ZOOMRESTORE Retore invisible zoom-axis to default
            % This get usually called by the "Restore"-Button
            if ~obj.isOctave && ~obj.isAppDesigner
                set(obj.axui,'XLim',[0,1],'YLim',[0,1]);
            end
        end % function
        
        function delete(obj)
            % DELETE Additional clean-up tasks on removal
            % When manually deleting the object from a GUI, some cleanup
            % may need to be done manually. This is still not the best way
            % of doing it, so far its a workaround when deleting at runtime
            try
                delete(obj.ax_p);
                delete(obj.ax_s);
                delete(obj.axplt);
                delete(obj.axdsp);
                delete(obj.axui);
                delete(obj.xlbl);
                delete(obj.ylbl);
            catch
            end
        end
    end % public methods
    
    % Private Methods
    methods (Access = private)
        function obj = axuiylimPostSetCallback(obj,~,~)
            % This Callback gets called after the invisible ui-axes was
            % zoomed or panned. It calculates the new limits for all other
            % axes and sets it properly to do the zooming.
            
            % Get the new relative axis limits which are on ui-axes now
            obj.xlimpost = get(obj.axui,'XLim');
            obj.ylimpost = get(obj.axui,'YLim');
            
            % X-Axes: Calculate new limits once and set it to primary axes.
            % as the axes are linked, this is sufficient.
            xlimold = get(obj.ax_p,'XLim');
            xlimnew(1) = (xlimold(2)-xlimold(1))./ ...
                (obj.xlimpre(2)-obj.xlimpre(1)).* ...
                (obj.xlimpost(1)-obj.xlimpre(1)) + xlimold(1);
            xlimnew(2) = (xlimold(2)-xlimold(1))./ ...
                (obj.xlimpre(2)-obj.xlimpre(1)).* ...
                (obj.xlimpost(2)-obj.xlimpre(1)) + xlimold(1);
            set(obj.ax_p,'XLim',xlimnew);
            
            % For each y axes now calculate the new limits relative to the
            % zoom box and apply it to the plot axes.
            
            ylimold = get(obj.ax_p,'YLim');
            % Calculate new Limits for each axis
            ylimnew(1) = (ylimold(2)-ylimold(1))./ ...
                (obj.ylimpre(2)-obj.ylimpre(1)).* ...
                (obj.ylimpost(1)-obj.ylimpre(1)) + ylimold(1);
            ylimnew(2) = (ylimold(2)-ylimold(1))./ ...
                (obj.ylimpre(2)-obj.ylimpre(1)).* ...
                (obj.ylimpost(2)-obj.ylimpre(1)) + ylimold(1);
            set(obj.ax_p,'YLim',ylimnew); % set it to axes
            
            ylimold = get(obj.ax_s,'YLim');
            % Calculate new Limits for each axis
            ylimnew(1) = (ylimold(2)-ylimold(1))./ ...
                (obj.ylimpre(2)-obj.ylimpre(1)).* ...
                (obj.ylimpost(1)-obj.ylimpre(1)) + ylimold(1);
            ylimnew(2) = (ylimold(2)-ylimold(1))./ ...
                (obj.ylimpre(2)-obj.ylimpre(1)).* ...
                (obj.ylimpost(2)-obj.ylimpre(1)) + ylimold(1);
            set(obj.ax_s,'YLim',ylimnew); % set it to axes
            
            if (obj.n >= 3) % for axes 3 and up:
                for idx = 1:obj.n-2 
                    % Read ylims from axes
                    ylimold = get(obj.axplt(idx),'YLim');
                    % Calculate new Limits for each axis
                    ylimnew(1) = (ylimold(2)-ylimold(1))./ ...
                        (obj.ylimpre(2)-obj.ylimpre(1)).* ...
                        (obj.ylimpost(1)-obj.ylimpre(1)) + ylimold(1);
                    ylimnew(2) = (ylimold(2)-ylimold(1))./ ...
                        (obj.ylimpre(2)-obj.ylimpre(1)).* ...
                        (obj.ylimpost(2)-obj.ylimpre(1)) + ylimold(1);
                    set(obj.axplt(idx),'YLim',ylimnew); % set it to axes
                end
            end % if
            
            % Set the relative pre-limits as post ones for next zoom
            % operation.
            obj.xlimpre = obj.xlimpost;
            obj.ylimpre = obj.ylimpost;
        end % function ylimPostSetCallback
        
        function storelims(obj)
            %STORELIMS stores the axis limits for Restore-functionality 
            obj.prevlims(1,:) = get(obj.ax_p,'XLim');
            obj.prevlims(2,:) = get(obj.ax_p,'YLim');
            obj.prevlims(3,:) = get(obj.ax_s,'YLim');
            if (obj.n >= 3) % for axes 3 and up
                for idx = 3:obj.n
                    obj.prevlims(idx+1,:) = get(obj.axplt(idx-2),'YLim');
                end
            end
            obj.limstored = true;
            obj.limsrestored = false;
        end
        
        function obj = axPylimPreSetCallback(obj,~,~)
            % This Callback gets called in App Designer Mode if the y
            % limits of the primary axes gets changed. It will store the
            % previous values.
            obj.xlimpre = get(obj.ax_p,'XLim');
            obj.ylimpre = get(obj.ax_p,'YLim');
        end % function
        
        function obj = axPylimPostSetCallback(obj,~,~)
            % This Callback gets called in App Designer Mode if the y
            % limits of the primary axes gets changed. It will sync all
            % other limits to make zooming in all axes possible.
            if obj.uiz || obj.uip % Only, if Zoom or Pan is active:
                % For each y axes now calculate the new limits relative to
                % the zoom box and apply it to the plot axes.
                
                % Get the new relative axis limits which are set now
                obj.xlimpost = get(obj.ax_p,'XLim');
                obj.ylimpost = get(obj.ax_p,'YLim');

                % Sync second axes
                ylimold = get(obj.ax_s,'YLim');
                % Calculate new Limits for each axis
                ylimnew(1) = (ylimold(2)-ylimold(1))./ ...
                    (obj.ylimpre(2)-obj.ylimpre(1)).* ...
                    (obj.ylimpost(1)-obj.ylimpre(1)) + ylimold(1);
                ylimnew(2) = (ylimold(2)-ylimold(1))./ ...
                    (obj.ylimpre(2)-obj.ylimpre(1)).* ...
                    (obj.ylimpost(2)-obj.ylimpre(1)) + ylimold(1);
                set(obj.ax_s,'YLim',ylimnew); % set it to axes

                if (obj.n >= 3) % for axes 3 and up:
                    for idx = 1:obj.n-2 
                        % Read ylims from axes
                        ylimold = get(obj.axplt(idx),'YLim');
                        % Calculate new Limits for each axis
                        ylimnew(1) = (ylimold(2)-ylimold(1))./ ...
                            (obj.ylimpre(2)-obj.ylimpre(1)).* ...
                            (obj.ylimpost(1)-obj.ylimpre(1)) + ylimold(1);
                        ylimnew(2) = (ylimold(2)-ylimold(1))./ ...
                            (obj.ylimpre(2)-obj.ylimpre(1)).* ...
                            (obj.ylimpost(2)-obj.ylimpre(1)) + ylimold(1);
                        set(obj.axplt(idx),'YLim',ylimnew); % set it to axes
                    end
                end % if
            end % if zoom or pan
        end % function axPylimPostSetCallback
        
        function obj = restorebtnCallback(obj,~,~)
            % Reset the AXUI to default size, triggering the above
            % callback to restore the original size.
            obj.zoomrestore();
        end
    end % private methods
end % classdef