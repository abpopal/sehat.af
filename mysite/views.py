from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from .models import Blood_Records, Blood_Group, Requests, User_Requests, PUser, Blood_Bank, Hospital, Donor
from .forms import EditProfileForm, DonorRegistrationForm, AddRecordForm, EditHospitalProfileForm
from accounts.models import User
# Create your views here.
def search_view(request):
    if request.method == 'GET':  # this will be GET now

        bloodname = request.GET.get('search').upper() # do some research what it does

        status = Blood_Records.objects.filter(bg_id__bg_name=bloodname)
        if request.user.is_authenticated and not request.user.is_hospital:
            try:
                donor = Donor.objects.get(user_id__username=request.user)
                status = status.exclude(d_id=donor)
            except Donor.DoesNotExist:
                donor = None

            status = status.filter(d_id__approved=True)


            return render(request, "search_result.html", {"record": status})
        else:
            status = status.exclude(d_id__approved=False)
            return render(request, "search_result.html", {"record": status})
    else:
        return render(request, "search_result.html", {})


def send_req_view(request, **kwargs):
    if request.method == 'GET':
        product = Blood_Records.objects.filter(record_id=kwargs.get('record_id', "")).first()
        print("from req view: ", product.record_id)

        req = Requests.create(product)
        req.save()
        usr = PUser.objects.get(username__username=request.user)
        ureq = User_Requests.create(req)
        ureq.user_id = usr
        ureq.save()
        return render(request, 'sendrequest.html', {'record': product})
    else:
        return render(request, 'sendrequest.html', {'msg': 'hello there'})


def profile_view(request):
    currentobj = request.user

    if currentobj.is_hospital:
        Hobj = Hospital.objects.get(h_username__username=currentobj.username)
        print(Hobj.name)
        return render(request, 'profile.html', {'user': currentobj, 'hospital': Hobj})

    else:
        Pobj = PUser.objects.get(username__username=currentobj)
        try:
            dobj = Donor.objects.get(user_id=Pobj)
        except Donor.DoesNotExist:
            dobj = None
        print(Pobj.username, dobj)
        return render(request, 'profile.html', {'user': currentobj, 'puser': Pobj, 'donor': dobj})


def req_view(request):
    if request.user.ishospital:
        hid = request.user
        try:
            hins = Hospital.objects.get(h_username=hid)
        except Hospital.DoesNotExist:
            hins = None
        try:
            bbid= Blood_Bank.objects.get(h_id=hins)
        except Blood_Bank.DoesNotExist:
            bbid = None

        try:
            myhreq = User_Requests.objects.filter(req_id__record_id__bb_id=bbid)
        except User_Requests.DoesNotExist:
            myhreq = None
        print("hospital", myhreq)
        return render(request, 'requests.html', {'hreqs': myhreq})
    else:

        try:
            myreq = User_Requests.objects.filter(req_id__record_id__d_id__user_id__username=request.user)
        except User_Requests.DoesNotExist:
            myreq = None
        print("user", myreq)
        return render(request, 'requests.html', {'reqs': myreq})





def edit_profile(request):
    if request.user.is_hospital:
        hobj = Hospital.objects.get(h_username__username=request.user)
        if request.method == 'POST':

            form = EditHospitalProfileForm(request.POST, instance=hobj)

            if form.is_valid():
                form.save()
                return redirect(reverse('profile'))
            else:
                args = {'form':form}
                return render(request, 'editprofile.html', args)
        else:
            form = EditHospitalProfileForm(instance=hobj)
            args = {'form': form}
            return render(request, 'editprofile.html', args)
    else:
        context = {}
        p_user = PUser.objects.get(username__username=request.user)
        if request.POST:
            print("form is post")
            form = EditProfileForm(request.POST, instance=p_user)

            if form.is_valid():
                print("validation passed")
                form.save()
                return redirect(reverse('profile'))
            else:
                args = {'form':form}
                return render(request, 'editprofile.html', args)


        else:
            print("not post")
            form = EditProfileForm(instance=p_user)
            args = {'form': form}
            return render(request, 'editprofile.html', args)


def home_view(request):
    return render(request, 'home.html', {})


def about_view(request):
    return render(request, 'about.html', {})

def delete_req_view(request, **kwargs):
    if request.method == 'GET':
        request = Requests.objects.filter(req_id=kwargs.get('req_id', "")).first()
        print("from dele req view: ", request.req_id)

        req = Requests.objects.get(req_id=request.req_id)
        req.delete()
        return redirect(reverse('requests'))
    else:
        return render(request, 'home.html', {})

def accept_req_view(request, **kwargs):
    if request.method == 'GET':
        request = Requests.objects.filter(req_id=kwargs.get('req_id', "")).first()
        print("from accept req view: ", request.req_id)

        req = Requests.objects.get(req_id=request.req_id)
        req.status = "Accepted"
        req.save()
        return redirect(reverse('requests'))
    else:
        return render(request, 'home.html', {})


def reject_req_view(request, **kwargs):
    if request.method == 'GET':
        request = Requests.objects.filter(req_id=kwargs.get('req_id', "")).first()
        print("from reject req view: ", request.req_id)

        req = Requests.objects.get(req_id=request.req_id)
        req.status = "Rejected"
        req.save()
        return redirect(reverse('requests'))
    else:
        return render(request, 'home.html', {})


def notification_view(request):
    myreqs = User_Requests.objects.filter(user_id__username=request.user)
    print(myreqs)
    return render(request, 'notification.html', {'reqs': myreqs})





def become_donor_view(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            p_user = PUser.objects.get(username=request.user)
            bgid = form.cleaned_data.get('bg_id')
            obj = Donor.objects.create(bg_id=bgid, user_id=p_user)
            obj.save()
            user = User.objects.get(username=request.user)
            user.isdonor = True
            user.save()

            blood_record_obj =Blood_Records.objects.create(quantity=1, d_id=obj, bg_id=obj.bg_id)

            return render(request, 'profile.html', {})
    else:
        form = DonorRegistrationForm()
        return render(request, 'donorform.html', {'form': form})

def add_record_view(request):
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            hid = Hospital.objects.get(h_username=request.user)

            rec_id = form.save()
            rec_id.bb_id = Blood_Bank.objects.get(h_id=hid)
            rec_id.save()
            return render(request, 'profile.html', {})
    else:
        form = AddRecordForm()
        return render(request, 'add_record.html', {'form': form})