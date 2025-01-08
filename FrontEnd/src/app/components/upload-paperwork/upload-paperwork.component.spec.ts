import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadPaperworkComponent } from './upload-paperwork.component';

describe('UploadPaperworkComponent', () => {
  let component: UploadPaperworkComponent;
  let fixture: ComponentFixture<UploadPaperworkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UploadPaperworkComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UploadPaperworkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
