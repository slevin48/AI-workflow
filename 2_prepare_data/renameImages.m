training_dataset = "2021-03-06-1";
dataFolder = "D:\devel\AI-workflow\samples2\"+training_dataset;
D = dir(dataFolder);
nameRoot = "img_";
for i = 4:numel(D) 
%   1 = .    
%   2 = ..
%   3 = data.csv
    if D(i).isdir == 0
        
        I = imread(fullfile(dataFolder, D(i).name));
        [~,filename,ext] = fileparts(D(i).name);
        nameLength = length( filename );
        if nameLength == 7
            continue;
        else
            if nameLength == 5
                imNumber = ["00" + filename(5)] ;
            elseif nameLength == 6
                imNumber = ["0" + filename(5:6)];                
            end
            newFilename = [nameRoot + imNumber + ext];
            imwrite(I, fullfile(dataFolder, newFilename));
            delete(fullfile(dataFolder, D(i).name));
        end
    end
end